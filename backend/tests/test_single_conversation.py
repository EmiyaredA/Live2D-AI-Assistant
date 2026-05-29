from __future__ import annotations

import pytest

from backend.conversations.single_conversation import process_single_conversation
from backend.core.agent.agent_interface import AgentOutput
from backend.core.service_context import ServiceContext


class MockAgent:
    def __init__(self):
        self._messages = [{"role": "system", "content": "test"}]

    async def chat(self, user_input: str):
        yield AgentOutput(display_text="Hello", tts_text="Hello", done=False)
        self._messages.append({"role": "assistant", "content": "Hello"})
        yield AgentOutput(display_text="Hello", tts_text="", done=True)

    async def close(self):
        pass


class MockTTS:
    async def async_generate_audio(self, text: str, file_name_no_ext: str) -> str:
        return ""


@pytest.mark.asyncio
async def test_single_conversation_pushes_messages():
    context = ServiceContext()
    context.agent_engine = MockAgent()
    context.tts_engine = MockTTS()
    context.live2d_model = None

    sent: list[dict] = []

    async def send(payload: dict):
        sent.append(payload)

    result = await process_single_conversation(
        context=context,
        websocket_send=send,
        user_input="hi",
        history_uid="test-uid",
    )

    assert result == "Hello"
    assert any(m.get("type") == "display-text" for m in sent)
    assert any(m.get("type") == "audio" for m in sent)
