from __future__ import annotations

from backend.core.agent.agent_interface import AgentInterface
from backend.core.agent.basic_agent import BasicMemoryAgent


class AgentFactory:
    @staticmethod
    def get_agent_engine(agent_type: str, **kwargs) -> AgentInterface:
        if agent_type in ("basic_memory", "openai", "default"):
            return BasicMemoryAgent(**kwargs)
        raise ValueError(f"Unsupported agent type: {agent_type}")
