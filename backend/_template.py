"""
app.py 参考模板（不参与运行）。

职责：创建 FastAPI 应用、生命周期（init_db）、CORS、注册 api 路由、挂载静态资源。
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.db import init_db
# from backend.api.chat import router as chat_router
# from backend.api.websocket_handler import init_ws_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Live2D AI Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
# app.include_router(init_ws_route(), prefix="/api/ws", tags=["websocket"])


@app.get("/")
def health():
    return {"status": "ok"}
