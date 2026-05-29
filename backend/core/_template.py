"""
service_context.py 参考模板（不参与运行）。

职责：按配置组装 ASR / TTS / Agent / Live2D，作为会话级 DI 容器。
复制到 service_context.py 后接入真实 Factory 与配置加载。
"""

from __future__ import annotations

from typing import Any


class ServiceContext:
    """每个 WebSocket 连接或会话持有一份上下文。"""

    def __init__(self) -> None:
        self.asr_engine: Any = None
        self.tts_engine: Any = None
        self.agent_engine: Any = None
        self.live2d_model: Any = None
        self.system_prompt: str = ""

    async def load_from_config(self, config: dict) -> None:
        # from backend.core.tts.tts_factory import TTSFactory
        # self.tts_engine = TTSFactory.get_tts_engine(
        #     config["tts_model"],
        #     **config.get("edge_tts", {}),
        # )
        # await self._init_asr(config)
        # await self._init_agent(config)
        # self._init_live2d(config.get("live2d_model_name", ""))
        raise NotImplementedError

    async def close(self) -> None:
        if self.agent_engine and hasattr(self.agent_engine, "close"):
            await self.agent_engine.close()
