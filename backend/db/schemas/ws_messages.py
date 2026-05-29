from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class EmbedTokenCreate(BaseModel):
    character_id: int
    allowed_origins: str = "*"
    expires_at: Optional[float] = None


class EmbedTokenRead(BaseModel):
    id: int
    character_id: int
    token: str
    allowed_origins: str
    expires_at: Optional[float]
    created_at: float


class EmbedPreview(BaseModel):
    character_id: int
    character_name: str
    persona_prompt: str
    live2d_model: Optional[dict[str, Any]] = None
    ws_url: str


class WSTextInput(BaseModel):
    type: str = "text-input"
    text: str
    history_uid: Optional[str] = None


class WSFetchCharacter(BaseModel):
    type: str = "fetch-character"
    character_id: Optional[int] = None
    embed_token: Optional[str] = None


class WSInterruptSignal(BaseModel):
    type: str = "interrupt-signal"
