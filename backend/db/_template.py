"""
db.py 与 models.py 参考模板（不参与运行）。

- 前半：数据库连接、Session、init_db → 合并到 db.py
- 后半：SQLModel 表定义 → 合并到 models.py
"""

from __future__ import annotations

import time
from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine

# ---------------------------------------------------------------------------
# 以下段落 → backend/db/db.py
# ---------------------------------------------------------------------------

DATABASE_URL = "sqlite:///./data/assistant.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    # import backend.db.models  # noqa: F401 — 确保 metadata 已注册
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# ---------------------------------------------------------------------------
# 以下段落 → backend/db/models.py
# ---------------------------------------------------------------------------


class CharacterConfig(SQLModel, table=True):
    """角色配置：人设、Live2D 模型名、TTS/ASR 选择等。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    persona_prompt: str = Field(default="")
    live2d_model_name: str = Field(default="")
    created_at: float = Field(default_factory=time.time)


class ChatHistory(SQLModel, table=True):
    """单次会话的消息记录。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    history_uid: str = Field(index=True)
    role: str  # human | ai
    content: str = Field(default="")
    created_at: float = Field(default_factory=time.time)
