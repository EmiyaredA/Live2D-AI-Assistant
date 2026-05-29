from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class Live2DModelCreate(BaseModel):
    name: str
    model_path: str = ""
    emotion_map: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Live2DModelUpdate(BaseModel):
    name: Optional[str] = None
    model_path: Optional[str] = None
    emotion_map: Optional[dict[str, Any]] = None
    metadata: Optional[dict[str, Any]] = None


class Live2DModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    name: str
    model_path: str
    emotion_map: dict[str, Any]
    metadata: dict[str, Any]
    created_at: float


class Live2DModelInfo(BaseModel):
    id: int
    name: str
    url: str
    emotion_map: dict[str, Any]
    metadata: dict[str, Any]
