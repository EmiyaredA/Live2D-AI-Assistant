from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class CharacterCreate(BaseModel):
    name: str
    persona_prompt: str = ""
    live2d_model_id: Optional[int] = None
    llm_config: dict[str, Any] = Field(default_factory=dict)
    tts_config: dict[str, Any] = Field(
        default_factory=lambda: {"engine": "edge_tts", "voice": "zh-CN-XiaoxiaoNeural"}
    )
    asr_config: dict[str, Any] = Field(default_factory=dict)
    mcp_config: dict[str, Any] = Field(default_factory=dict)
    skill_ids: list[str] = Field(default_factory=list)


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    persona_prompt: Optional[str] = None
    live2d_model_id: Optional[int] = None
    llm_config: Optional[dict[str, Any]] = None
    tts_config: Optional[dict[str, Any]] = None
    asr_config: Optional[dict[str, Any]] = None
    mcp_config: Optional[dict[str, Any]] = None
    skill_ids: Optional[list[str]] = None


class CharacterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    name: str
    persona_prompt: str
    live2d_model_id: Optional[int]
    llm_config: dict[str, Any]
    tts_config: dict[str, Any]
    asr_config: dict[str, Any]
    mcp_config: dict[str, Any]
    skill_ids: list[str]
    created_at: float
