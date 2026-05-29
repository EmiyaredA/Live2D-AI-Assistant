from __future__ import annotations

import uuid
from typing import Any, Callable

from backend.conversations.single_conversation import process_single_conversation
from backend.core.service_context import ServiceContext

WebSocketSend = Callable[[dict[str, Any]], Any]


async def handle_conversation_trigger(
    context: ServiceContext,
    websocket_send: WebSocketSend,
    user_input: str,
    history_uid: str | None = None,
) -> str:
    uid = history_uid or str(uuid.uuid4())
    return await process_single_conversation(
        context=context,
        websocket_send=websocket_send,
        user_input=user_input,
        history_uid=uid,
    )
