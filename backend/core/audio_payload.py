from __future__ import annotations

import base64
from pathlib import Path
from typing import Any


def prepare_audio_payload(
    audio_path: str | None,
    display_text: str | None = None,
    actions: dict[str, Any] | None = None,
    chunk_length_ms: int = 20,
) -> dict[str, Any]:
    if not audio_path:
        return {
            "type": "audio",
            "audio": None,
            "volumes": [],
            "slice_length": chunk_length_ms,
            "display_text": {"text": display_text or "", "name": "AI"},
            "actions": actions,
        }

    path = Path(audio_path)
    audio_b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "audio",
        "audio": audio_b64,
        "volumes": [],
        "slice_length": chunk_length_ms,
        "display_text": {"text": display_text or "", "name": "AI"},
        "actions": actions,
    }
