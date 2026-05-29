"""
API DTO 参考模板（不参与运行）。

职责：描述 HTTP 请求/响应 JSON 形状，与 ORM（models.py）分离。
复制到 schemas/chat.py 等正式模块后使用。
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ChatMessageCreate(BaseModel):
    text: str


class ChatMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str
    content: str


class CharacterConfigRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    persona_prompt: str
    live2d_model_name: str
