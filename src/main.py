import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.custom import LoggingMiddleware
from src.custom.cst_exceptions import AppExceptionError
from src.custom.cst_lifespan import app_lifespan  # lifespan pakai DataService
from src.mlogg import init_logging, logger
from src.router import register_routes

init_logging()
app = FastAPI(lifespan=app_lifespan)

# Mask sensitive fields di logs
app.add_middleware(LoggingMiddleware, mask_fields=["password", "token", "secret"])

register_routes(app)


# Register exception handlers
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


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint.

    This endpoint serves as the entry point for the API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Otomax API Forwarder"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
