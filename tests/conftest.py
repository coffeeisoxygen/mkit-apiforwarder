import sys
from pathlib import Path

import pytest
from loguru import logger
from src.config import Settings


@pytest.fixture(scope="session", autouse=True)
def configure_loguru():
    logger.remove()  # Hapus default handler
    logger.add(
        sink=sys.stderr,
        format="<level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG",
        backtrace=True,
        diagnose=True,
        colorize=True,
    )


@pytest.fixture(autouse=True)
def intercept_loguru(caplog):
    handler_id = logger.add(caplog.handler, format="{message}", level="DEBUG")
    yield
    logger.remove(handler_id)


PATHTOENVS = Path(__file__).resolve().parent.parent / ".env.test"


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    # Use a test-specific .env file if needed
    settings = Settings(_env_file=PATHTOENVS, _env_file_encoding="utf-8")  # type: ignore
    settings.app_env = "test"
    settings.app_debug = True
    settings.app_name = "test_app"
    assert settings.app_env == "test"
    print("Loaded settings:", settings.model_dump())
    return settings
