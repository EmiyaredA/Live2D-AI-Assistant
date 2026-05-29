from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ASRInterface(Protocol):
    async def async_transcribe_np(self, audio: Any) -> str:
        ...
