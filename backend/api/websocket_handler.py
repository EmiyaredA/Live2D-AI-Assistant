from __future__ import annotations

import json
import time
import uuid
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlmodel import Session, select

from backend.conversations.conversation_handler import handle_conversation_trigger
from backend.core.service_context import ServiceContext
from backend.db.db import engine
from backend.db.models import CharacterConfig, ChatHistory, EmbedToken, Live2DModel
from backend.db.schemas.serializers import parse_json_field

router = APIRouter()


class WebSocketHandler:
    def __init__(self) -> None:
        self._contexts: dict[str, ServiceContext] = {}

    async def handle_connection(self, websocket: WebSocket) -> None:
        client_uid = str(uuid.uuid4())
        await websocket.accept()
        context = ServiceContext()
        self._contexts[client_uid] = context

        try:
            while True:
                raw = await websocket.receive_text()
                data = json.loads(raw)
                msg_type = data.get("type")

                if msg_type == "fetch-character":
                    await self._handle_fetch_character(websocket, context, data)
                elif msg_type == "text-input":
                    await self._handle_text_input(websocket, context, data)
                elif msg_type == "interrupt-signal":
                    context.interrupt()
                else:
                    await websocket.send_json(
                        {"type": "error", "message": f"Unknown message type: {msg_type}"}
                    )
        except WebSocketDisconnect:
            pass
        finally:
            await context.close()
            self._contexts.pop(client_uid, None)

    async def _handle_fetch_character(
        self,
        websocket: WebSocket,
        context: ServiceContext,
        data: dict[str, Any],
    ) -> None:
        character_id = data.get("character_id")
        embed_token = data.get("embed_token")

        with Session(engine) as session:
            character, live2d_row = self._resolve_character(
                session, character_id, embed_token
            )
            if character is None:
                await websocket.send_json({"type": "error", "message": "Character not found"})
                return

            await context.load_from_character(character, live2d_row)
            await websocket.send_json(
                {
                    "type": "set-model-and-conf",
                    "character_id": character.id,
                    "character_name": character.name,
                    "model_info": context.model_info,
                    "history_uid": data.get("history_uid") or str(uuid.uuid4()),
                }
            )

    async def _handle_text_input(
        self,
        websocket: WebSocket,
        context: ServiceContext,
        data: dict[str, Any],
    ) -> None:
        if context.agent_engine is None:
            await websocket.send_json(
                {"type": "error", "message": "Send fetch-character before text-input"}
            )
            return

        text = (data.get("text") or "").strip()
        if not text:
            return

        history_uid = data.get("history_uid") or str(uuid.uuid4())

        async def send(payload: dict[str, Any]) -> None:
            await websocket.send_json(payload)

        await handle_conversation_trigger(
            context=context,
            websocket_send=send,
            user_input=text,
            history_uid=history_uid,
        )

        if context.character_id:
            self._persist_history(context.character_id, history_uid, text, context)

    def _persist_history(
        self,
        character_id: int,
        history_uid: str,
        user_text: str,
        context: ServiceContext,
    ) -> None:
        ai_text = ""
        if hasattr(context.agent_engine, "_messages"):
            msgs = context.agent_engine._messages
            if len(msgs) > 1 and msgs[-1]["role"] == "assistant":
                ai_text = msgs[-1]["content"]

        with Session(engine) as session:
            session.add(
                ChatHistory(
                    character_id=character_id,
                    history_uid=history_uid,
                    role="human",
                    content=user_text,
                )
            )
            if ai_text:
                session.add(
                    ChatHistory(
                        character_id=character_id,
                        history_uid=history_uid,
                        role="ai",
                        content=ai_text,
                    )
                )
            session.commit()

    def _resolve_character(
        self,
        session: Session,
        character_id: int | None,
        embed_token: str | None,
    ) -> tuple[CharacterConfig | None, Live2DModel | None]:
        if embed_token:
            token_row = session.exec(
                select(EmbedToken).where(EmbedToken.token == embed_token)
            ).first()
            if token_row is None:
                return None, None
            if token_row.expires_at is not None and token_row.expires_at < time.time():
                return None, None
            character_id = token_row.character_id

        if character_id is None:
            return None, None

        character = session.get(CharacterConfig, character_id)
        if character is None:
            return None, None

        live2d_row = None
        if character.live2d_model_id:
            live2d_row = session.get(Live2DModel, character.live2d_model_id)

        return character, live2d_row


_handler = WebSocketHandler()


def init_ws_routes() -> APIRouter:
    @router.websocket("/client-ws")
    async def client_ws(websocket: WebSocket) -> None:
        await _handler.handle_connection(websocket)

    return router
