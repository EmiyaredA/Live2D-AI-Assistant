"""
api 路由参考模板（不参与运行）。

职责：HTTP 薄层 — 校验入参、调用 core、返回 schemas。
复制到 chat.py 等正式模块；WebSocket 建议单独 websocket_handler.py。
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from backend.db.db import get_session

# 正式实现：from backend.db.schemas.chat import ChatMessageCreate, ChatMessageRead


class ChatMessageCreate(BaseModel):
    text: str


class ChatMessageRead(BaseModel):
    role: str
    content: str

router = APIRouter()


def get_context():
    """占位：正式实现从 backend.core.service_context 提供会话级引擎。"""
    raise NotImplementedError("wire ServiceContext in app lifespan or Depends")


@router.post("/message", response_model=ChatMessageRead)
async def send_text(
    body: ChatMessageCreate,
    session: Session = Depends(get_session),
    ctx=Depends(get_context),
):
    # reply_text = ""
    # async for chunk in ctx.agent_engine.chat(body.text):
    #     reply_text += chunk
    # return ChatMessageRead(role="ai", content=reply_text)
    return ChatMessageRead(role="ai", content="placeholder")
