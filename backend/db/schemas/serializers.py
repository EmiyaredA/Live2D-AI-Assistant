from __future__ import annotations

import json
from typing import Any

from backend.db.models import CharacterConfig, Live2DModel


def parse_json_field(raw: str, default: Any) -> Any:
    if not raw:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return default


def character_to_read(char: CharacterConfig) -> dict[str, Any]:
    return {
        "id": char.id,
        "tenant_id": char.tenant_id,
        "name": char.name,
        "persona_prompt": char.persona_prompt,
        "live2d_model_id": char.live2d_model_id,
        "llm_config": parse_json_field(char.llm_config, {}),
        "tts_config": parse_json_field(char.tts_config, {}),
        "asr_config": parse_json_field(char.asr_config, {}),
        "mcp_config": parse_json_field(char.mcp_config, {}),
        "skill_ids": parse_json_field(char.skill_ids, []),
        "created_at": char.created_at,
    }


def live2d_model_to_read(model: Live2DModel) -> dict[str, Any]:
    return {
        "id": model.id,
        "tenant_id": model.tenant_id,
        "name": model.name,
        "model_path": model.model_path,
        "emotion_map": parse_json_field(model.emotion_map, {}),
        "metadata": parse_json_field(model.metadata_json, {}),
        "created_at": model.created_at,
    }
