from __future__ import annotations

from pathlib import Path

import edge_tts

from backend.core.settings import get_settings
from backend.core.tts.tts_interface import TTSInterface


class EdgeTTSEngine:
    def __init__(self, voice: str = "zh-CN-XiaoxiaoNeural") -> None:
        self.voice = voice

    async def async_generate_audio(self, text: str, file_name_no_ext: str) -> str:
        if not text.strip():
            raise ValueError("TTS text is empty")
        settings = get_settings()
        out_path = settings.audio_cache_dir / f"{file_name_no_ext}.mp3"
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(str(out_path))
        return str(out_path)


class TTSFactory:
    @staticmethod
    def get_tts_engine(engine_type: str, **kwargs) -> TTSInterface:
        if engine_type == "edge_tts":
            return EdgeTTSEngine(voice=kwargs.get("voice", "zh-CN-XiaoxiaoNeural"))
        raise ValueError(f"Unsupported TTS engine: {engine_type}")
