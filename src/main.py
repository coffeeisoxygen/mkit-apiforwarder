import uvicorn
from fastapi import FastAPI

from src.utils.mlogger import init_custom_logging

app = FastAPI()
init_custom_logging()


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI entry point is running."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
