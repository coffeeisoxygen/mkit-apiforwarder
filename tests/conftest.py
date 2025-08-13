from pathlib import Path

import pytest
from loguru import logger
from src.config import get_settings

PATHTOTESTENV = Path(__file__).resolve().parent.parent / ".env.test"


@pytest.fixture(autouse=True)
def intercept_loguru(caplog):
    """
    Intercept all Loguru logs and redirect them to pytest's caplog handler.
    """
    handler_id = logger.add(
        sink=caplog.handler,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        enqueue=False,  # pakai True kalau spawn child process
    )
    yield
    logger.remove(handler_id)


@pytest.fixture(scope="session", autouse=True)
def override_settings():
    """
    Clear cache and load test environment settings once per test session.
    """
    get_settings.cache_clear()
    get_settings(_env_file=str(PATHTOTESTENV))
    get_settings(_env_file=str(PATHTOTESTENV))
