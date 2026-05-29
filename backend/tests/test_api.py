from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.core.live2d_model import Live2dModel
from backend.core.settings import get_settings
from backend.db.db import init_db

ADMIN_HEADERS = {"X-Admin-API-Key": "dev-admin-key"}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("ASSISTANT_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("ADMIN_API_KEY", "dev-admin-key")
    get_settings.cache_clear()
    init_db()
    with TestClient(app) as test_client:
        yield test_client
    get_settings.cache_clear()


def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_live2d_emotion_extraction():
    model = Live2dModel({"emotion_map": {"joy": 0, "sad": 1}})
    text, actions = model.extract_emotion("[joy] Hello there!")
    assert "joy" not in text.lower() or "[" not in text
    assert actions.expressions == [0]


def test_character_crud(client):
    model_resp = client.post(
        "/v1/live2d-models",
        headers=ADMIN_HEADERS,
        json={"name": "test-model", "emotion_map": {"joy": 0}},
    )
    assert model_resp.status_code == 201
    model_id = model_resp.json()["id"]

    char_resp = client.post(
        "/v1/characters",
        headers=ADMIN_HEADERS,
        json={
            "name": "test-char",
            "persona_prompt": "You are helpful.",
            "live2d_model_id": model_id,
        },
    )
    assert char_resp.status_code == 201
    char_id = char_resp.json()["id"]

    list_resp = client.get("/v1/characters", headers=ADMIN_HEADERS)
    assert any(c["id"] == char_id for c in list_resp.json())

    patch_resp = client.patch(
        f"/v1/characters/{char_id}",
        headers=ADMIN_HEADERS,
        json={"name": "updated-char"},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["name"] == "updated-char"


def test_embed_token_and_preview(client):
    char_resp = client.post(
        "/v1/characters",
        headers=ADMIN_HEADERS,
        json={"name": "embed-char", "persona_prompt": "hi"},
    )
    char_id = char_resp.json()["id"]

    token_resp = client.post(
        "/v1/embed-tokens",
        headers=ADMIN_HEADERS,
        json={"character_id": char_id, "allowed_origins": "*"},
    )
    assert token_resp.status_code == 201
    token = token_resp.json()["token"]

    preview = client.get("/v1/embed/preview", params={"token": token})
    assert preview.status_code == 200
    assert preview.json()["character_id"] == char_id

    invalid = client.get("/v1/embed/preview", params={"token": "invalid"})
    assert invalid.status_code == 401
