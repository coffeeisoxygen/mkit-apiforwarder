from pathlib import Path

import pytest
from loguru import logger
from src.config import get_settings
from src.utils.mlogger import init_custom_logging


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    init_custom_logging()


@pytest.fixture(autouse=True)
def intercept_loguru(caplog):
    handler_id = logger.add(caplog.handler, format="{message}", level="DEBUG")
    yield
    logger.remove(handler_id)


PATHTOENVS = Path(__file__).resolve().parent.parent / ".env.test"


@pytest.fixture(scope="session", autouse=True)
def override_settings():
    get_settings.cache_clear()
    get_settings(_env_file=".env.test")
