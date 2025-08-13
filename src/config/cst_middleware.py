import json
import time
import uuid

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


def mask_body_fields(body_data: dict, mask_fields: list[str]) -> dict:
    """Mask field sensitif di body."""
    for field in mask_fields:
        if field in body_data:
            body_data[field] = "***MASKED***"
    return body_data


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, mask_fields: list[str] | None = None):
        super().__init__(app)
        self.mask_fields = mask_fields or []

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Inject request_id ke loguru context
        logger_ctx = logger.contextualize(request_id=request_id)

        try:
            # --- Baca body (tanpa makan stream) ---
            body_bytes = await request.body()
            request._body = body_bytes
            try:
                body_data = json.loads(body_bytes.decode("utf-8"))
                body_data = mask_body_fields(body_data, self.mask_fields)
            except Exception:
                body_data = None

            # --- Log Request ---
            logger.bind(request_id=request_id).info({
                "event": "request_in",
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
                "query": dict(request.query_params) or None,
                "body": body_data,
            })

            # --- Jalankan endpoint ---
            response = await call_next(request)

            process_time = (time.perf_counter() - start_time) * 1000

            # --- Log Response ---
            logger.bind(request_id=request_id).info({
                "event": "response_out",
                "status_code": response.status_code,
                "time_ms": round(process_time, 2),
                "content_length": response.headers.get("content-length"),
            })

            return response

        finally:
            del logger_ctx  # bersihkan context
