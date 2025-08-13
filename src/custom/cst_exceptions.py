# src/exception/exceptions.py

from src.config import get_settings

APP_NAME = get_settings().app_name


# =========================
# Base & Specific Exceptions
# =========================
class AppExceptionError(Exception):
    """Base exception with adapter support."""

    default_message: str = "An application error occurred."
    status_code: int = 500

    def __init__(
        self,
        message: str | None = None,
        name: str = APP_NAME,
        context: dict | None = None,
        cause: Exception | None = None,
    ):
        self.message = message or self.default_message
        self.name = name
        self.context = context or {}
        self.__cause__ = cause
        super().__init__(self.message)


class InternalError(AppExceptionError):
    default_message = "Internal server error."
    status_code = 500


class ServiceError(AppExceptionError):
    default_message = "Service is unavailable."
    status_code = 503


class ValidationError(AppExceptionError):
    default_message = "Validation failed."
    status_code = 422


class FileLoaderError(AppExceptionError):
    default_message = "Failed to load file."
    status_code = 400
