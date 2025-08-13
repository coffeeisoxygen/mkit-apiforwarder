import functools
from collections.abc import Callable

from src.mlogg.config import logger


def logtrace_endpoint(endpoint_name: str | None = None) -> Callable:
    """Decorator to log the start and end of an endpoint function."""

    def decorator(func: Callable) -> Callable:
        name = endpoint_name or func.__name__

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"Executing endpoint: '{name}'")
            result = await func(*args, **kwargs)
            logger.info(f"Finished endpoint: '{name}'")
            return result

        return wrapper

    return decorator


endpoint_logger = logtrace_endpoint
