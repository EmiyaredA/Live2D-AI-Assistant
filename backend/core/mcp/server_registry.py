from __future__ import annotations

from typing import Any


class MCPServerRegistry:
  """Phase 1 skeleton — Phase 2 will load mcp_servers.json and manage stdio processes."""

  def __init__(self, config: dict[str, Any] | None = None) -> None:
    self.config = config or {}
    self.enabled_servers: list[str] = self.config.get("enabled_servers", [])

  async def list_tools(self) -> list[dict[str, Any]]:
    return []

  async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
    raise NotImplementedError("MCP runtime is planned for Phase 2")
