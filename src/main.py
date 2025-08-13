import uvicorn
from fastapi import FastAPI

from src.custom import LoggingMiddleware
from src.custom.cst_lifespan import app_lifespan

app = FastAPI(lifespan=app_lifespan)

app.add_middleware(LoggingMiddleware, mask_fields=["password", "token", "secret"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Otomax API Forwarder",
    }


@app.get("/health")
async def health_check():
    member_repo = getattr(app.state, "member_repo", None)
    member_watcher = getattr(app.state, "member_watcher", None)
    return {
        "status": "healthy",
        "member_repo_type": str(type(member_repo)),
        "member_repo_repr": str(member_repo),
        "member_watcher_type": str(type(member_watcher)),
        "member_watcher_repr": str(member_watcher),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
