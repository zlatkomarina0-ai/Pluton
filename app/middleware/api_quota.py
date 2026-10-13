import logging
from typing import Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.services.quota_service import ApiQuotaService

logger = logging.getLogger("pluton.api_quota")


class ApiQuotaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api") and not request.url.path.startswith("/api/health"):
            allowed = ApiQuotaService.allow_request(request, limit=100)
            if not allowed:
                logger.warning(
                    "API quota exceeded for request path=%s client=%s",
                    request.url.path,
                    request.client.host if request.client else "unknown",
                )
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "API quota exceeded for today. Maximum 100 requests/day.",
                        "limit": 100,
                        "reset": "daily at UTC midnight",
                    },
                )

        return await call_next(request)
