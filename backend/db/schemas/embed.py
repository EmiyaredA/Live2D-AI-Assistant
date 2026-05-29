from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


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
