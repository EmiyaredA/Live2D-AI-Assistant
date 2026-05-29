from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.core.agent.agent_factory import AgentFactory
from backend.core.agent.basic_agent import BasicMemoryAgent  # noqa: F401
from backend.core.asr.asr_factory import ASRFactory
from backend.core.live2d_model import Live2dModel, build_model_info_from_db
from backend.core.settings import ROOT_DIR
from backend.core.skills.loader import load_skill_summaries
from backend.core.tts.tts_factory import TTSFactory
from backend.db.schemas.serializers import parse_json_field


class ServiceContext:
    def __init__(self) -> None:
        self.asr_engine: Any = None
        self.tts_engine: Any = None
        self.agent_engine: Any = None
        self.live2d_model: Live2dModel | None = None
        self.system_prompt: str = ""
        self.character_id: int | None = None
        self.character_name: str = ""
        self.history_uid: str = ""
        self.model_info: dict[str, Any] = {}

    async def load_from_character(self, character: Any, live2d_row: Any | None) -> None:
        self.character_id = character.id
        self.character_name = character.name

        tts_config = parse_json_field(character.tts_config, {"engine": "edge_tts"})
        asr_config = parse_json_field(character.asr_config, {"engine": "none"})
        llm_config = parse_json_field(character.llm_config, {})
        skill_ids = parse_json_field(character.skill_ids, [])

        self.tts_engine = TTSFactory.get_tts_engine(
            tts_config.get("engine", "edge_tts"),
            **{k: v for k, v in tts_config.items() if k != "engine"},
        )
        self.asr_engine = ASRFactory.get_asr_engine(
            asr_config.get("engine", "none"),
            **{k: v for k, v in asr_config.items() if k != "engine"},
        )

        self.system_prompt = self.construct_system_prompt(
            character.persona_prompt,
            live2d_row,
            skill_ids,
        )

        self.agent_engine = AgentFactory.get_agent_engine(
            llm_config.get("engine", "basic_memory"),
            system_prompt=self.system_prompt,
            model=llm_config.get("model"),
            api_key=llm_config.get("api_key"),
            base_url=llm_config.get("base_url"),
        )

        if live2d_row:
            emotion_map = parse_json_field(live2d_row.emotion_map, {})
            metadata = parse_json_field(live2d_row.metadata_json, {})
            self.model_info = build_model_info_from_db(
                live2d_row.id,
                live2d_row.name,
                live2d_row.model_path,
                emotion_map,
                metadata,
            )
            self.live2d_model = Live2dModel(self.model_info)
        else:
            self.model_info = {}
            self.live2d_model = Live2dModel({"emotion_map": {}})

    def construct_system_prompt(
        self,
        persona_prompt: str,
        live2d_row: Any | None,
        skill_ids: list[str],
    ) -> str:
        parts = [persona_prompt.strip() or "You are a helpful AI assistant."]

        live2d_prompt_path = ROOT_DIR / "prompts" / "utils" / "live2d_expression_prompt.txt"
        if live2d_prompt_path.exists() and live2d_row:
            emo_map = parse_json_field(live2d_row.emotion_map, {})
            emo_keys = " ".join(f"[{k}]" for k in emo_map.keys())
            live2d_prompt = live2d_prompt_path.read_text(encoding="utf-8")
            live2d_prompt = live2d_prompt.replace("[<insert_emomap_keys>]", emo_keys)
            parts.append(live2d_prompt.strip())

        skill_summary = load_skill_summaries(skill_ids)
        if skill_summary:
            parts.append(skill_summary)

        return "\n\n".join(parts)

    def interrupt(self) -> None:
        if isinstance(self.agent_engine, BasicMemoryAgent):
            self.agent_engine.interrupt()

    async def close(self) -> None:
        if self.agent_engine and hasattr(self.agent_engine, "close"):
            await self.agent_engine.close()
