import inspect
import logging
import sys
from pathlib import Path

from loguru import logger
from loguru_config import LoguruConfig

CONFIG_PATH = Path(__file__).parent.parent.parent / "loguru.yaml"


def normalize_level(level: str) -> str:
    """Normalize the logging level string."""
    return level.upper() if isinstance(level, str) else level


class InterceptHandler(logging.Handler):
    """Intercept standard logging and forward to loguru with correct format."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1
        msg = record.getMessage()
        # Remove double INFO: for uvicorn.access logs
        if record.name == "uvicorn.access" and msg.startswith("INFO:"):
            msg = msg[5:].lstrip()
        logger.opt(depth=depth, exception=record.exc_info).log(level, msg)


class StreamToLogger:
    """Redirect stdout/stderr to loguru."""

    def __init__(self, level: str = "INFO"):
        self._level = normalize_level(level)

    def write(self, buffer: str):
        for line in buffer.rstrip().splitlines():
            logger.opt(depth=1).log(self._level, line.rstrip())

    def flush(self):
        # No-op for compatibility
        pass

    def isatty(self):
        return False


def init_logging():
    """Centralized logging setup for the whole app.

    Loads loguru config from YAML before intercepting standard logging.
    Ensures all logs (including intercepted) use the YAML format.
    """
    LoguruConfig.load(str(CONFIG_PATH))
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
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
    sys.stdout = StreamToLogger("INFO")
    sys.stderr = StreamToLogger("ERROR")
    logger.debug("🔄 Centralized logging initialized")
