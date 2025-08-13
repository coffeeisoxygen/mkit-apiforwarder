from config import get_settings

APP_NAME = get_settings().app_name


class AppExceptionError(Exception):
    """Base application exception with adapter support."""

    default_message: str = "An application error occurred."
    status_code: int = 500

    def __init__(
        self,
        message: str | None = None,
        name: str = APP_NAME,
        context: dict | None = None,
        cause: Exception | None = None,  # simpan original exception
    ):
        self.message = message or self.default_message
        self.name = name
        self.context = context or {}
        self.__cause__ = cause  # built-in Python cause chaining
        super().__init__(self.message)


class ServiceError(AppExceptionError):
    """Failures in external services or APIs."""

    default_message = "Service is unavailable."
    status_code = 503


class FileLoaderError(AppExceptionError):
    """File loading errors."""

    default_message = "Failed to load file."
    status_code = 400
