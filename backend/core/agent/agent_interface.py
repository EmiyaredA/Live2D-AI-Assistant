from __future__ import annotations

from dataclasses import dataclass, field
from typing import AsyncIterator, Protocol, runtime_checkable


@dataclass
class AgentOutput:
    display_text: str = ""
    tts_text: str = ""
    done: bool = False


@runtime_checkable
class AgentInterface(Protocol):
    async def chat(self, user_input: str) -> AsyncIterator[AgentOutput]:
        ...

    async def close(self) -> None:
        ...
