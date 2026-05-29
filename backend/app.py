from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.characters import router as characters_router
from backend.api.embed import router as embed_router
from backend.api.live2d_models import router as live2d_models_router
from backend.api.websocket_handler import init_ws_routes
from backend.core.settings import get_settings
from backend.db.db import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Live2D AI Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters_router)
app.include_router(live2d_models_router)
app.include_router(embed_router)
app.include_router(init_ws_routes(), prefix="/api/ws", tags=["websocket"])

live2d_dir = Path(settings.live2d_models_dir)
live2d_dir.mkdir(parents=True, exist_ok=True)
app.mount(
    "/live2d-models",
    StaticFiles(directory=str(live2d_dir), follow_symlink=True),
    name="live2d-models",
)


@app.get("/")
def health():
    return {"status": "ok", "service": "live2d-ai-assistant"}
