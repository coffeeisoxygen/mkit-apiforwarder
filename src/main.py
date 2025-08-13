import uvicorn
from fastapi import FastAPI

from src.config import DEVELOPMENT_ENV_FILE, get_settings
from src.mlogg import init_custom_logging

settings = get_settings(_env_file=DEVELOPMENT_ENV_FILE)
init_custom_logging(settings.app_env)

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Hello, FastAPI entry point is running.",
        "env": settings.app_env,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
