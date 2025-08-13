"""Custom log configurations with Loguru + YAML."""

import logging
import sys
from pathlib import Path

from loguru import logger
from loguru_config import LoguruConfig

from src.config import get_settings
from src.mlogg.config import InterceptHandler, StreamToLogger

settings = get_settings()
PATHLOGAPPCONFIG = Path(__file__).resolve().parent.parent.parent / "logging.yaml"


class CustomLogger:
    def __init__(self, env: str | None = None, config_path: Path | None = None):
        self.env = env or settings.app_env
        self.config_path = config_path or PATHLOGAPPCONFIG

    def configure_uvicorn_logging(self):
        uvicorn_loggers = (
            "uvicorn",
            "uvicorn.error",
            "uvicorn.access",
            "uvicorn.asgi",
            "uvicorn.warning",
            "uvicorn.server",
            "uvicorn.info",
        )
        for logger_name in uvicorn_loggers:
            uvicorn_logger = logging.getLogger(logger_name)
            uvicorn_logger.handlers = [InterceptHandler()]
            uvicorn_logger.propagate = False
        access_logger = logging.getLogger("uvicorn.access")
        access_logger.setLevel(logging.INFO)
        logger.debug("🔄 Uvicorn logging configured to use loguru")

    def redirect_streams(self):
        sys.stdout = StreamToLogger("INFO")
        sys.stderr = StreamToLogger("ERROR")
        logger.debug("🔄 stdout/stderr redirected to loguru")

    def init(self):
        LoguruConfig.load(str(self.config_path))
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
        logger.bind().debug(f"we are running in {self.env} mode")
        logger.bind().debug("🔄 Python logging intercepted")
        self.configure_uvicorn_logging()
        self.redirect_streams()


custom_logger = CustomLogger()


def init_custom_logging(env: str | None = None, config_path: Path | None = None):
    custom_logger = CustomLogger(env, config_path)
    custom_logger.init()
