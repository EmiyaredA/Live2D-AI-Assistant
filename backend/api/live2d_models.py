from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session, select

from backend.api.deps import require_admin_api_key
from backend.core.live2d_model import build_model_info_from_db
from backend.core.settings import get_settings
from backend.db.db import get_session
from backend.db.models import Live2DModel
from backend.db.schemas.live2d_model import (
    Live2DModelCreate,
    Live2DModelInfo,
    Live2DModelRead,
    Live2DModelUpdate,
)
from backend.db.schemas.serializers import live2d_model_to_read, parse_json_field

router = APIRouter(prefix="/v1/live2d-models", tags=["live2d-models"])


@router.get("", response_model=list[Live2DModelRead])
def list_models(
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> list[dict[str, Any]]:
    rows = session.exec(select(Live2DModel).order_by(Live2DModel.id)).all()
    return [live2d_model_to_read(row) for row in rows]


@router.post("", response_model=Live2DModelRead, status_code=status.HTTP_201_CREATED)
def create_model(
    body: Live2DModelCreate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> dict[str, Any]:
    row = Live2DModel(
        name=body.name,
        model_path=body.model_path,
        emotion_map=json.dumps(body.emotion_map),
        metadata_json=json.dumps(body.metadata),
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return live2d_model_to_read(row)


@router.get("/{model_id}", response_model=Live2DModelRead)
def get_model(
    model_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> dict[str, Any]:
    row = session.get(Live2DModel, model_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return live2d_model_to_read(row)


@router.get("/{model_id}/info", response_model=Live2DModelInfo)
def get_model_info(model_id: int, session: Session = Depends(get_session)) -> Live2DModelInfo:
    row = session.get(Live2DModel, model_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Model not found")

    emotion_map = parse_json_field(row.emotion_map, {})
    metadata = parse_json_field(row.metadata_json, {})
    info = build_model_info_from_db(
        row.id, row.name, row.model_path, emotion_map, metadata
    )
    return Live2DModelInfo(
        id=info["id"],
        name=info["name"],
        url=info["url"],
        emotion_map=emotion_map,
        metadata=metadata,
    )


@router.patch("/{model_id}", response_model=Live2DModelRead)
def update_model(
    model_id: int,
    body: Live2DModelUpdate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> dict[str, Any]:
    row = session.get(Live2DModel, model_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Model not found")

    data = body.model_dump(exclude_unset=True)
    if "emotion_map" in data and data["emotion_map"] is not None:
        data["emotion_map"] = json.dumps(data["emotion_map"])
    if "metadata" in data and data["metadata"] is not None:
        data["metadata_json"] = json.dumps(data.pop("metadata"))

    for key, value in data.items():
        setattr(row, key, value)

    session.add(row)
    session.commit()
    session.refresh(row)
    return live2d_model_to_read(row)


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(
    model_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> None:
    row = session.get(Live2DModel, model_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Model not found")
    session.delete(row)
    session.commit()


@router.post("/{model_id}/upload", response_model=Live2DModelRead)
async def upload_model_files(
    model_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> dict[str, Any]:
    row = session.get(Live2DModel, model_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Model not found")

    settings = get_settings()
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in row.name)
    target_dir = settings.live2d_models_dir / safe_name
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = Path(file.filename or "upload.bin").name
    dest = target_dir / filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    if filename.endswith(".model3.json"):
        row.model_path = f"{safe_name}/{filename}"

    session.add(row)
    session.commit()
    session.refresh(row)
    return live2d_model_to_read(row)
