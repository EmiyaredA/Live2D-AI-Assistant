from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TTSInterface(Protocol):
    async def async_generate_audio(self, text: str, file_name_no_ext: str) -> str:
        """Return path to generated audio file."""
        ...
