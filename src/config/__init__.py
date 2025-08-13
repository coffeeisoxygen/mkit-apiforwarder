"""project environments configurations."""

import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_env: str
    app_debug: bool
    app_name: str

    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings(_env_file: str | Path | None = None) -> Settings:
    """Prioritas:.

    1. Argumen _env_file
    2. ENV_FILE dari environment variable
    3. DEFAULT_ENV_FILE (.env)
    """
    env_file = _env_file or os.getenv("ENV_FILE", DEFAULT_ENV_FILE)
    return Settings(_env_file=env_file, _env_file_encoding="utf-8")  # type: ignore


# default instance
settings = get_settings()
