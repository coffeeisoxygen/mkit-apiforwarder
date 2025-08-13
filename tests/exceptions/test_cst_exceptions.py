from src.custom.cst_exceptions import (
    AppExceptionError,
    FileLoaderError,
    ServiceError,
)


def test_app_exception_error_defaults():
    exc = AppExceptionError()
    assert exc.message == "An application error occurred."
    assert exc.status_code == 500
    assert isinstance(exc, Exception)
    assert exc.name is not None
    assert exc.context == {}


def test_app_exception_error_custom_message_and_context():
    exc = AppExceptionError(
        message="Custom error",
        context={"foo": "bar"},
    )
    assert exc.message == "Custom error"
    assert exc.context == {"foo": "bar"}


def test_app_exception_error_cause():
    cause = ValueError("original")
    exc = AppExceptionError(cause=cause)
    assert exc.__cause__ == cause


def test_service_error_defaults():
    exc = ServiceError()
    assert exc.message == "Service is unavailable."
    assert exc.status_code == 503


def test_file_loader_error_defaults():
    exc = FileLoaderError()
    assert exc.message == "Failed to load file."
    assert exc.status_code == 400
