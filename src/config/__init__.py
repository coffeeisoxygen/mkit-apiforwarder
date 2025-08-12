from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PATHTOENVS = Path(__file__).resolve().parent.parent.parent / ".env"
# LISTENVS = (
#     # str(PATHTOENVS / ".env.dev"),  # first Load
#     # str(PATHTOENVS / ".env.test"),  # second Load
#     # str(PATHTOENVS / ".env"),  # third Load
# )


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


# @lru_cache
# def get_settings(env_file: Path | None = PATHTOENVS) -> Settings:
#     """Get application settings.

#     This function retrieves the application settings from the specified environment file.

#     Args:
#         env_file (Path | None, optional): The path to the environment file. Defaults to PATHTOENVS.

#     Returns:
#         Settings: The application settings.
#     """
#     return Settings(env_file=env_file, env_file_encoding="utf-8")  # type: ignore
