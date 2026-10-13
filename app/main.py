from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.config import settings
from app.middleware.api_quota import ApiQuotaMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.routers.sources import router as sources_router

app = FastAPI(title="PLUTON Core", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ApiQuotaMiddleware)

app.include_router(sources_router)

# scheduler start is optional, controlled by ENABLE_SCHEDULER env var
if settings.ENABLE_SCHEDULER:
    try:
        from app.scheduler import start_scheduler_in_thread

        start_scheduler_in_thread(interval_seconds=settings.SCHEDULER_INTERVAL_SECONDS)
    except Exception:
        pass


@app.get("/")
def root():
    return {
        "service": "PLUTON",
        "status": "online",
        "phase": "8-hardening",
        "message": "PLUTON core API is running.",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "PLUTON",
        "phase": "8-hardening",
        "database": "ready",
        "frontend": "available",
    }


@app.get("/api/summary")
def summary():
    return {
        "project": "PLUTON",
        "stack": ["FastAPI", "PostgreSQL", "SQLAlchemy", "Alembic"],
        "modules": ["users", "sports", "leagues", "teams", "fixtures", "predictions"],
        "status": "operational",
    }
