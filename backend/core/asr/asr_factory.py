from __future__ import annotations

from typing import Any

from backend.core.asr.asr_interface import ASRInterface


class NoopASREngine:
    async def async_transcribe_np(self, audio: Any) -> str:
        raise NotImplementedError("ASR is not configured; use text input")


class ASRFactory:
    @staticmethod
    def get_asr_engine(engine_type: str, **kwargs) -> ASRInterface:
        if engine_type in ("none", "noop", ""):
            return NoopASREngine()
        raise ValueError(f"Unsupported ASR engine: {engine_type}")
