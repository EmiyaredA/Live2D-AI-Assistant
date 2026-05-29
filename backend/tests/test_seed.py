from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from backend.core.settings import get_settings
from backend.db.db import init_db
from backend.db.models import CharacterConfig, Live2DModel
from backend.db.seed import seed_live2d_models


@pytest.fixture()
def seeded_env(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    models_dir = tmp_path / "live2d-models"
    models_dir.mkdir()
    (models_dir / "mao_pro" / "runtime").mkdir(parents=True)
    (models_dir / "mao_pro" / "runtime" / "mao_pro.model3.json").write_text("{}")

    catalog_dir = tmp_path / "config"
    catalog_dir.mkdir()
    catalog = [
        {
            "name": "mao_pro",
            "model_path": "mao_pro/runtime/mao_pro.model3.json",
            "emotion_map": {"joy": 3},
            "metadata": {"description": "test"},
        }
    ]
    (catalog_dir / "live2d_catalog.json").write_text(json.dumps(catalog))

    monkeypatch.setenv("ASSISTANT_DATA_DIR", str(data_dir))
    get_settings.cache_clear()

    import backend.core.settings as settings_mod
    import backend.db.seed as seed_mod

    monkeypatch.setattr(settings_mod, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(seed_mod, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(settings_mod.Settings, "model_config", settings_mod.Settings.model_config)

    # Re-bind live2d_models_dir via patched ROOT in get_settings
    get_settings.cache_clear()

    init_db()
    yield tmp_path
    get_settings.cache_clear()


def test_seed_live2d_models_from_catalog(seeded_env, monkeypatch):
    import backend.db.seed as seed_mod
    import backend.core.settings as settings_mod

    monkeypatch.setattr(settings_mod, "ROOT_DIR", seeded_env)
    monkeypatch.setattr(seed_mod, "ROOT_DIR", seeded_env)
    get_settings.cache_clear()

    from backend.db.db import engine

    with Session(engine) as session:
        ids = seed_live2d_models(session)
        assert "mao_pro" in ids

        row = session.exec(select(Live2DModel).where(Live2DModel.name == "mao_pro")).first()
        assert row is not None
        assert row.model_path == "mao_pro/runtime/mao_pro.model3.json"

        char = session.exec(
            select(CharacterConfig).where(CharacterConfig.name == "Mao 助手")
        ).first()
        # demo character seeded by init_db -> seed_all
        assert char is not None
