from __future__ import annotations

import secrets
import time
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from sqlmodel import Session, select

from backend.api.deps import require_admin_api_key
from backend.core.live2d_model import build_model_info_from_db
from backend.db.db import get_session
from backend.db.models import CharacterConfig, EmbedToken, Live2DModel
from backend.db.schemas.embed import EmbedPreview, EmbedTokenCreate, EmbedTokenRead
from backend.db.schemas.serializers import parse_json_field

router = APIRouter(prefix="/v1", tags=["embed"])


def _validate_embed_token(
    session: Session,
    token: str,
    origin: str | None,
) -> EmbedToken:
    row = session.exec(select(EmbedToken).where(EmbedToken.token == token)).first()
    if row is None:
        raise HTTPException(status_code=401, detail="Invalid embed token")

    if row.expires_at is not None and row.expires_at < time.time():
        raise HTTPException(status_code=401, detail="Embed token expired")

    allowed = row.allowed_origins.strip()
    if allowed != "*" and origin:
        allowed_list = [o.strip() for o in allowed.split(",") if o.strip()]
        if origin not in allowed_list:
            raise HTTPException(status_code=403, detail="Origin not allowed")

    return row


@router.post("/embed-tokens", response_model=EmbedTokenRead, status_code=status.HTTP_201_CREATED)
def create_embed_token(
    body: EmbedTokenCreate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> EmbedToken:
    character = session.get(CharacterConfig, body.character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    row = EmbedToken(
        character_id=body.character_id,
        token=secrets.token_urlsafe(32),
        allowed_origins=body.allowed_origins,
        expires_at=body.expires_at,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


@router.get("/embed-tokens", response_model=list[EmbedTokenRead])
def list_embed_tokens(
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> list[EmbedToken]:
    return list(session.exec(select(EmbedToken).order_by(EmbedToken.id)).all())


@router.delete("/embed-tokens/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_embed_token(
    token_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> None:
    row = session.get(EmbedToken, token_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Token not found")
    session.delete(row)
    session.commit()


@router.get("/embed/preview", response_model=EmbedPreview)
def embed_preview(
    request: Request,
    token: str = Query(...),
    session: Session = Depends(get_session),
    origin: str | None = Header(default=None, alias="Origin"),
) -> EmbedPreview:
    embed_row = _validate_embed_token(session, token, origin)
    character = session.get(CharacterConfig, embed_row.character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    live2d_info: dict[str, Any] | None = None
    if character.live2d_model_id:
        model = session.get(Live2DModel, character.live2d_model_id)
        if model:
            emotion_map = parse_json_field(model.emotion_map, {})
            metadata = parse_json_field(model.metadata_json, {})
            live2d_info = build_model_info_from_db(
                model.id, model.name, model.model_path, emotion_map, metadata
            )

    ws_scheme = "wss" if request.url.scheme == "https" else "ws"
    ws_url = f"{ws_scheme}://{request.url.netloc}/api/ws/client-ws"

    return EmbedPreview(
        character_id=character.id,
        character_name=character.name,
        persona_prompt=character.persona_prompt,
        live2d_model=live2d_info,
        ws_url=ws_url,
    )
