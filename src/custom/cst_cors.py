"""setup cors."""

from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://127.0.0.1",
        ],  # Allow all origins, adjust as needed
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
