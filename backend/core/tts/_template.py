"""
TTS 插件参考模板（不参与运行）。

结构：TTSInterface（契约）+ TTSFactory（按配置选实现）+ 具体引擎。
复制时拆成 tts_interface.py、tts_factory.py、edge_tts.py 等正式文件。
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TTSInterface(Protocol):
    async def async_generate_audio(self, text: str, file_name_no_ext: str) -> str:
        """返回生成的音频文件路径（相对 URL 或绝对路径）。"""
        ...


class EdgeTTSEngine:
    def __init__(self, voice: str = "zh-CN-XiaoxiaoNeural") -> None:
        self.voice = voice

    async def async_generate_audio(self, text: str, file_name_no_ext: str) -> str:
        raise NotImplementedError("integrate edge-tts or chosen backend")


class TTSFactory:
    @staticmethod
    def get_tts_engine(engine_type: str, **kwargs) -> TTSInterface:
        if engine_type == "edge_tts":
            return EdgeTTSEngine(voice=kwargs.get("voice", "zh-CN-XiaoxiaoNeural"))
        raise ValueError(f"Unsupported TTS engine: {engine_type}")
