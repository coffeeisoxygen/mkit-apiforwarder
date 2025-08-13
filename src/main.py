import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.custom import LoggingMiddleware
from src.custom.cst_exceptions import AppExceptionError
from src.custom.cst_lifespan import app_lifespan  # lifespan pakai DataService
from src.dependencies.dep_data import DepMemberAuthService
from src.mlogg import logger
from src.router import register_routes
from src.service.auth.srv_memberauth import MemberTrxRequestModel

app = FastAPI(lifespan=app_lifespan)

# Mask sensitive fields di logs
app.add_middleware(LoggingMiddleware, mask_fields=["password", "token", "secret"])


register_routes(app)


# Global exception handler for custom exceptions
@app.exception_handler(AppExceptionError)
async def app_exception_handler(request: Request, exc: AppExceptionError):  # noqa: ARG001, D103, RUF029
    logger.error(f"Application error: {exc.message}", extra=exc.context)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "context": exc.context},
    )


# Root endpoint
@logger.catch
@app.get("/")
async def root():
    """Root endpoint.

    This endpoint serves as the entry point for the API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Otomax API Forwarder"}


@logger.catch
@app.get("/health")
async def health_check():
    """Health check endpoint.

    This endpoint can be used to check the health of the API.

    Returns:
        dict: A health status message.
    """
    return {"status": "healthy"}


@app.get("/sample-auth")
async def sample_auth(
    request: MemberTrxRequestModel,
    member_auth_service: DepMemberAuthService,
):
    """Sample endpoint to demonstrate MemberAuthService usage."""
    member = member_auth_service.authenticate_and_verify(request)
    return {"memberid": member.memberid, "is_active": member.is_active}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
