"""Custom log configurations with Loguru + YAML."""

import inspect
import logging
import sys
from pathlib import Path

from loguru import logger
from loguru_config import LoguruConfig

from src.config import get_settings

settings = get_settings()

PATHLOGAPPCONFIG = Path(__file__).resolve().parent.parent.parent / "logapp_config.yaml"
PATHLOGTESTCONFIG = (
    Path(__file__).resolve().parent.parent.parent / "logtest_config.yaml"
)


# --- Interceptor untuk logging bawaan Python ---
class InterceptHandler(logging.Handler):
    """A logging handler that intercepts standard Python logging records.

    and forwards them to Loguru, preserving the original log context.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Cari frame asal log
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# --- Patch logging Uvicorn ---
def configure_uvicorn_logging():
    """Configures Uvicorn loggers to use Loguru for logging output.

    Replaces Uvicorn's default handlers with InterceptHandler.
    """
    uvicorn_loggers = (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "uvicorn.asgi",
    )
    for logger_name in uvicorn_loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [InterceptHandler()]
        uvicorn_logger.propagate = False

    access_logger = logging.getLogger("uvicorn.access")
    access_logger.setLevel(logging.INFO)

    logger.debug("🔄 Uvicorn logging configured to use loguru")


# --- Normalisasi level ---
def normalize_level(level: str) -> str:
    """Normalizes a logging level to uppercase string if it's a string.

    otherwise returns the level unchanged.
    """
    return level.upper() if isinstance(level, str) else level


# --- Redirect stdout/stderr ke Loguru ---
class StreamToLogger:
    """Redirects writes to a Loguru logger at the specified level.

    Useful for redirecting stdout and stderr to Loguru.
    """

    def __init__(self, level: str = "INFO"):
        self._level = normalize_level(level)

    def write(self, buffer: str):
        """Writes each line of the buffer to the Loguru logger."""
        for line in buffer.rstrip().splitlines():
            logger.opt(depth=1).log(self._level, line.rstrip())

    def flush(self):
        """No-op flush method to satisfy file-like interface."""
        pass

    def isatty(self):
        """Returns False to indicate this is not an interactive stream."""
        return False


# --- Init Logging ---
def init_custom_logging():
    """Inisialisasi logging kustom untuk aplikasi.

    Mengatur konfigurasi logging menggunakan Loguru dan mengalihkan
    output standar ke logger.
    """
    # Deteksi environment dari settings
    env = get_settings().app_env

    if "pytest" in sys.modules or env == "testing":
        LoguruConfig.load(str(PATHLOGTESTCONFIG))
        # Tambahkan extra field 'testing' jika di testing
        with logger.contextualize(testing=True):
            logger.bind().debug("🔄 Loguru configured for testing")
        return

    if env == "development":
        with logger.contextualize(development=True):
            logger.info(f" we running in {env} mode")
        return
    # 1. Pre-configure Loguru dari YAML
    LoguruConfig.load(str(PATHLOGAPPCONFIG))
    logger.bind().debug("✅ Loguru pre-configured from YAML")

    # 2. Intercept semua logging bawaan Python
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    logger.bind().debug("🔄 Python logging intercepted")

    # 3. Patch uvicorn logging
    configure_uvicorn_logging()

    # 4. Redirect print & error ke loguru
    sys.stdout = StreamToLogger("INFO")
    sys.stderr = StreamToLogger("ERROR")
    logger.debug("🔄 stdout/stderr redirected to loguru")
