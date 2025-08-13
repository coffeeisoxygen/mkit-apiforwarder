"""project environments configurations."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PATHTOENVS = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    app_env: str
    app_debug: bool
    app_name: str

    model_config = SettingsConfigDict(
        env_file=PATHTOENVS,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


pathtodevenv = Path(__file__).resolve().parent.parent.parent / ".env.dev"
settings = Settings(_env_file=pathtodevenv, _env_file_encoding="utf-8")  # type: ignore


@lru_cache
def get_settings() -> Settings:
    """Get settings with cache."""
    return settings
