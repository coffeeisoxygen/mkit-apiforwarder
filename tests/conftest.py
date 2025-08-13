from pathlib import Path

import pytest
from dotenv import load_dotenv
from src.config import get_settings
from src.mlogg import logger

PATHTOTESTENV = Path(__file__).parent.parent / ".env.test"


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    # Load .env.test ke os.environ, override env vars yang ada
    load_dotenv(dotenv_path=PATHTOTESTENV, override=True)

    get_settings.cache_clear()
    settings = get_settings()  # sekarang ambil dari os.environ yang sudah di-override

    assert PATHTOTESTENV.exists(), f".env.test file not found at {PATHTOTESTENV}"
    assert settings.app_env == "TESTING", (
        f"Expected app_env=TESTING but got {settings.app_env}"
    )

    print(f"Test env loaded app_env={settings.app_env}")


@pytest.fixture(autouse=True)
def intercept_loguru(caplog):
    handler_id = logger.add(
        sink=caplog.handler,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        enqueue=False,
    )
    yield
    logger.remove(handler_id)
