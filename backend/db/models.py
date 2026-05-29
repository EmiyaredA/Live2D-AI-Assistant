from __future__ import annotations

import time
from typing import Optional

from sqlmodel import Field, SQLModel


class Tenant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: float = Field(default_factory=time.time)


class Live2DModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(default=1, index=True)
    name: str = Field(index=True)
    model_path: str = Field(default="")
    emotion_map: str = Field(default="{}")
    metadata_json: str = Field(default="{}")
    created_at: float = Field(default_factory=time.time)


class CharacterConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(default=1, index=True)
    name: str = Field(index=True)
    persona_prompt: str = Field(default="")
    live2d_model_id: Optional[int] = Field(default=None, index=True)
    llm_config: str = Field(default="{}")
    tts_config: str = Field(default='{"engine": "edge_tts", "voice": "zh-CN-XiaoxiaoNeural"}')
    asr_config: str = Field(default="{}")
    mcp_config: str = Field(default="{}")
    skill_ids: str = Field(default="[]")
    created_at: float = Field(default_factory=time.time)


class EmbedToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(default=1, index=True)
    character_id: int = Field(index=True)
    token: str = Field(index=True, unique=True)
    allowed_origins: str = Field(default="*")
    expires_at: Optional[float] = Field(default=None)
    created_at: float = Field(default_factory=time.time)


class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(default=1, index=True)
    character_id: int = Field(index=True)
    history_uid: str = Field(index=True)
    role: str
    content: str = Field(default="")
    created_at: float = Field(default_factory=time.time)
