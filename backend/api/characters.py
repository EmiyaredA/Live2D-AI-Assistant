from __future__ import annotations

import json
import secrets
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend.api.deps import require_admin_api_key
from backend.db.db import get_session
from backend.db.models import CharacterConfig, Live2DModel
from backend.db.schemas.character import CharacterCreate, CharacterRead, CharacterUpdate
from backend.db.schemas.serializers import character_to_read, parse_json_field

router = APIRouter(prefix="/v1/characters", tags=["characters"])


@router.get("", response_model=list[CharacterRead])
def list_characters(
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> list[dict[str, Any]]:
    rows = session.exec(select(CharacterConfig).order_by(CharacterConfig.id)).all()
    return [character_to_read(row) for row in rows]


@router.post("", response_model=CharacterRead, status_code=status.HTTP_201_CREATED)
def create_character(
    body: CharacterCreate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> dict[str, Any]:
    if body.live2d_model_id is not None:
        model = session.get(Live2DModel, body.live2d_model_id)
        if model is None:
            raise HTTPException(status_code=404, detail="Live2D model not found")

    row = CharacterConfig(
        name=body.name,
        persona_prompt=body.persona_prompt,
        live2d_model_id=body.live2d_model_id,
        llm_config=json.dumps(body.llm_config),
        tts_config=json.dumps(body.tts_config),
        asr_config=json.dumps(body.asr_config),
        mcp_config=json.dumps(body.mcp_config),
        skill_ids=json.dumps(body.skill_ids),
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return character_to_read(row)


@router.get("/{character_id}", response_model=CharacterRead)
def get_character(
    character_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> dict[str, Any]:
    row = session.get(CharacterConfig, character_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character_to_read(row)


@router.patch("/{character_id}", response_model=CharacterRead)
def update_character(
    character_id: int,
    body: CharacterUpdate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> dict[str, Any]:
    row = session.get(CharacterConfig, character_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Character not found")

    data = body.model_dump(exclude_unset=True)
    if "live2d_model_id" in data and data["live2d_model_id"] is not None:
        model = session.get(Live2DModel, data["live2d_model_id"])
        if model is None:
            raise HTTPException(status_code=404, detail="Live2D model not found")

    for field in ("llm_config", "tts_config", "asr_config", "mcp_config", "skill_ids"):
        if field in data and data[field] is not None:
            data[field] = json.dumps(data[field])

    for key, value in data.items():
        setattr(row, key, value)

    session.add(row)
    session.commit()
    session.refresh(row)
    return character_to_read(row)


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(
    character_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin_api_key),
) -> None:
    row = session.get(CharacterConfig, character_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Character not found")
    session.delete(row)
    session.commit()
