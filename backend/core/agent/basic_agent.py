from __future__ import annotations

from typing import AsyncIterator

from openai import AsyncOpenAI

from backend.core.agent.agent_interface import AgentInterface, AgentOutput
from backend.core.settings import get_settings


class BasicMemoryAgent:
    def __init__(
        self,
        system_prompt: str,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        max_history: int = 20,
    ) -> None:
        settings = get_settings()
        self.system_prompt = system_prompt
        self.model = model or settings.openai_model
        self.max_history = max_history
        self._messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]
        self._client = AsyncOpenAI(
            api_key=api_key or settings.openai_api_key or "not-set",
            base_url=base_url or settings.openai_base_url,
        )
        self._interrupted = False

    def interrupt(self) -> None:
        self._interrupted = True

    async def chat(self, user_input: str) -> AsyncIterator[AgentOutput]:
        self._interrupted = False
        self._messages.append({"role": "user", "content": user_input})
        self._trim_history()

        stream = await self._client.chat.completions.create(
            model=self.model,
            messages=self._messages,
            stream=True,
        )

        full_text = ""
        async for chunk in stream:
            if self._interrupted:
                break
            delta = chunk.choices[0].delta.content or ""
            if not delta:
                continue
            full_text += delta
            yield AgentOutput(display_text=full_text, tts_text=delta, done=False)

        if full_text:
            self._messages.append({"role": "assistant", "content": full_text})
        yield AgentOutput(display_text=full_text, tts_text="", done=True)

    def _trim_history(self) -> None:
        system = self._messages[:1]
        rest = self._messages[1:]
        if len(rest) > self.max_history:
            rest = rest[-self.max_history :]
        self._messages = system + rest

    async def close(self) -> None:
        await self._client.close()


