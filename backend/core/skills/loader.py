from __future__ import annotations

from pathlib import Path

from backend.core.settings import ROOT_DIR

SKILLS_DIR = ROOT_DIR / "prompts" / "skills"


def load_skill_summaries(skill_ids: list[str]) -> str:
    if not skill_ids:
        return ""

    summaries: list[str] = []
    for skill_id in skill_ids:
        skill_path = SKILLS_DIR / skill_id / "SKILL.md"
        if not skill_path.exists():
            continue
        content = skill_path.read_text(encoding="utf-8")
        first_line = content.strip().splitlines()[0] if content.strip() else skill_id
        summaries.append(f"- {skill_id}: {first_line[:200]}")

    if not summaries:
        return ""

    return "Available skills:\n" + "\n".join(summaries)
