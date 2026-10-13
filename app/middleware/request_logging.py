import json
import logging
import time
import uuid
from datetime import datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("pluton.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
        start = time.time()

        try:
            response = await call_next(request)
            duration_ms = round((time.time() - start) * 1000, 2)
            logger.info(
                json.dumps({
                    "event": "request",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "client": request.client.host if request.client else None,
                })
            )
            response.headers["x-request-id"] = request_id
            return response
        except Exception as exc:
            duration_ms = round((time.time() - start) * 1000, 2)
            logger.exception(
                json.dumps({
                    "event": "request_error",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                    "client": request.client.host if request.client else None,
                    "error": str(exc),
                })
            )
            raise
