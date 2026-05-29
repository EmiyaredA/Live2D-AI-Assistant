from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    assistant_data_dir: Path = ROOT_DIR / "data"
    assistant_host: str = "0.0.0.0"
    assistant_port: int = 8000

    admin_api_key: str = "dev-admin-key"
    default_tenant_id: int = 1

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def database_url(self) -> str:
        db_path = self.assistant_data_dir / "assistant.db"
        return f"sqlite:///{db_path}"

    @property
    def live2d_models_dir(self) -> Path:
        return ROOT_DIR / "live2d-models"

    @property
    def audio_cache_dir(self) -> Path:
        return self.assistant_data_dir / "audio_cache"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.assistant_data_dir.mkdir(parents=True, exist_ok=True)
    settings.audio_cache_dir.mkdir(parents=True, exist_ok=True)
    settings.live2d_models_dir.mkdir(parents=True, exist_ok=True)
    return settings
