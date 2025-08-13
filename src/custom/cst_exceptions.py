# src/exception/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.mlogg import logger

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


# =========================
# FastAPI Exception Handler
# =========================
async def register_exception_handlers(app):
    @app.exception_handler(AppExceptionError)
    async def app_exception_handler(request: Request, exc: AppExceptionError):
        logger.exception(f"Exception occurred: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.name,
                "message": exc.message,
                "context": exc.context,
            },
        )
