import inspect
import logging

from loguru import logger


def normalize_level(level: str) -> str:
    """Normalize the logging level.

    This function takes a logging level as a string and normalizes it to a standard format.

    Args:
        level (str): The logging level to normalize.

    Returns:
        str: The normalized logging level.
    """
    return level.upper() if isinstance(level, str) else level


class InterceptHandler(logging.Handler):
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
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class StreamToLogger:
    def __init__(self, level: str = "INFO"):
        self._level = normalize_level(level)

    def write(self, buffer: str):
        for line in buffer.rstrip().splitlines():
            logger.opt(depth=1).log(self._level, line.rstrip())

    def flush(self):
        """Just a placeholder."""
        pass

    def isatty(self):
        return False
