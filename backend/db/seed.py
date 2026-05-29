from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlmodel import Session, select

from backend.core.settings import ROOT_DIR, get_settings
from backend.db.models import CharacterConfig, Live2DModel

CATALOG_PATH = ROOT_DIR / "config" / "live2d_catalog.json"


def _load_catalog() -> list[dict[str, Any]]:
    if not CATALOG_PATH.exists():
        return []
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _model_files_exist(model_path: str) -> bool:
    settings = get_settings()
    return (settings.live2d_models_dir / model_path).exists()


def seed_live2d_models(session: Session) -> dict[str, int]:
    """Seed bundled models from catalog when files are present. Returns name -> id."""
    name_to_id: dict[str, int] = {}
    settings = get_settings()

    for entry in _load_catalog():
        name = entry["name"]
        model_path = entry["model_path"]
        if not _model_files_exist(model_path):
            continue

        existing = session.exec(select(Live2DModel).where(Live2DModel.name == name)).first()
        if existing:
            name_to_id[name] = existing.id  # type: ignore[assignment]
            continue

        row = Live2DModel(
            tenant_id=settings.default_tenant_id,
            name=name,
            model_path=model_path,
            emotion_map=json.dumps(entry.get("emotion_map", {})),
            metadata_json=json.dumps(
                {
                    "description": entry.get("description", ""),
                    **entry.get("metadata", {}),
                }
            ),
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        name_to_id[name] = row.id  # type: ignore[assignment]

    return name_to_id


def seed_demo_characters(session: Session, model_ids: dict[str, int]) -> None:
    settings = get_settings()
    demos = [
        {
            "name": "Mao 助手",
            "model": "mao_pro",
            "persona_prompt": (
                "你是 Mao，一位活泼可爱的二次元 AI 助手。"
                "说话简短自然，偶尔用 [joy]、[surprise] 等表情标签。"
            ),
        },
        {
            "name": "Shizuku 助手",
            "model": "shizuku",
            "persona_prompt": (
                "你是 Shizuku，温柔安静的二次元 AI 助手。"
                "语气轻柔，适当使用 [joy]、[neutral] 等表情标签。"
            ),
        },
    ]

    for demo in demos:
        model_id = model_ids.get(demo["model"])
        if model_id is None:
            continue

        existing = session.exec(
            select(CharacterConfig).where(CharacterConfig.name == demo["name"])
        ).first()
        if existing:
            continue

        session.add(
            CharacterConfig(
                tenant_id=settings.default_tenant_id,
                name=demo["name"],
                persona_prompt=demo["persona_prompt"],
                live2d_model_id=model_id,
            )
        )

    session.commit()


def seed_all() -> None:
    from backend.db.db import engine

    with Session(engine) as session:
        model_ids = seed_live2d_models(session)
        seed_demo_characters(session, model_ids)
