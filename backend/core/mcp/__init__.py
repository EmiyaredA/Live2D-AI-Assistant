from __future__ import annotations

from typing import Any

from backend.core.mcp.server_registry import MCPServerRegistry


async def get_mcp_tools(mcp_config: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    """Phase 1 stub — returns empty tools. Phase 2 wires MCPServerRegistry."""
    registry = MCPServerRegistry(mcp_config)
    tools = await registry.list_tools()
    prompt = ""
    if mcp_config.get("enabled_servers"):
        prompt = "MCP tools are configured but runtime is not enabled in Phase 1."
    return tools, prompt
