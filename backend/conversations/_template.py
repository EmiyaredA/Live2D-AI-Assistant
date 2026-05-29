"""
对话编排参考模板（不参与运行）。

职责：串联 ASR → Agent 流式输出 → 分句/表情 → TTS → WebSocket 推送。
复制到 single_conversation.py；触发与打断放在 conversation_handler.py。
"""

from __future__ import annotations

from typing import Any, Callable, Union

import numpy as np

WebSocketSend = Callable[[dict], Any]


async def process_single_conversation(
    context: Any,
    websocket_send: WebSocketSend,
    client_uid: str,
    user_input: Union[str, np.ndarray],
    session_emoji: str = "🙂",
) -> str:
    """
    处理一轮单人对话。

    Args:
        context: ServiceContext，含 asr_engine / agent_engine / tts_engine
        websocket_send: 向前端推送 JSON 的回调
        user_input: 文本或音频 ndarray
    """
    full_response = ""

    # 1. 若是音频，先 ASR
    # input_text = user_input if isinstance(user_input, str) else await context.asr_engine.async_transcribe_np(user_input)

    # 2. Agent 流式输出
    # async for output in context.agent_engine.chat(input_text):
    #     if hasattr(output, "display_text"):
    #         await websocket_send({"type": "display-text", "text": output.display_text})
    #     if hasattr(output, "tts_text"):
    #         audio_path = await context.tts_engine.async_generate_audio(output.tts_text, ...)
    #         await websocket_send({"type": "audio", "path": audio_path})
    #         full_response += output.tts_text

    return full_response
