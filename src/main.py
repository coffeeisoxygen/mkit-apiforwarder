import uvicorn
from fastapi import FastAPI

from src.custom import LoggingMiddleware
from src.custom.cst_lifespan import app_lifespan  # lifespan pakai DataService
from src.router import register_routes

app = FastAPI(lifespan=app_lifespan)

# Mask sensitive fields di logs
app.add_middleware(LoggingMiddleware, mask_fields=["password", "token", "secret"])

register_routes(app)


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
