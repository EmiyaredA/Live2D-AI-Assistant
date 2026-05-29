from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ChatMessageCreate(BaseModel):
    text: str


class ChatMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str
    content: str
