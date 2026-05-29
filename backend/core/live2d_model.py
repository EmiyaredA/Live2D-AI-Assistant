from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Actions:
    expressions: list[int | str] = field(default_factory=list)
    motions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"expressions": self.expressions, "motions": self.motions}


class Live2dModel:
    def __init__(self, model_info: dict[str, Any]) -> None:
        self.model_info = model_info
        emo_map = model_info.get("emotion_map") or model_info.get("emotionMap") or {}
        self.emo_map: dict[str, Any] = {k.lower(): v for k, v in emo_map.items()}
        self.emo_str = " ".join(f"[{key}]" for key in self.emo_map.keys())

    def extract_emotion(self, text: str) -> tuple[str, Actions]:
        actions = Actions()
        cleaned = text
        for keyword, value in self.emo_map.items():
            pattern = re.compile(rf"\[{re.escape(keyword)}\]", re.IGNORECASE)
            if pattern.search(cleaned):
                actions.expressions.append(value)
                cleaned = pattern.sub("", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned, actions

    def remove_emotion_keywords(self, text: str) -> str:
        cleaned, _ = self.extract_emotion(text)
        return cleaned


def build_model_info_from_db(
    model_id: int,
    name: str,
    model_path: str,
    emotion_map: dict[str, Any],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    url = f"/live2d-models/{model_path.lstrip('/')}" if model_path else ""
    info = {
        "id": model_id,
        "name": name,
        "url": url,
        "emotion_map": emotion_map,
        "emotionMap": emotion_map,
        **metadata,
    }
    return info
