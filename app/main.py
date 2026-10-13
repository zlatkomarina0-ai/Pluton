from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers.sources import router as sources_router

app = FastAPI(title="PLUTON Core", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sources_router)

# scheduler start is optional, controlled by ENABLE_SCHEDULER env var
if os.getenv("ENABLE_SCHEDULER", "false").lower() == "true":
    try:
        from app.scheduler import start_scheduler_in_thread

        start_scheduler_in_thread(interval_seconds=int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "60")))
    except Exception:
        pass


@app.get("/")
def root():
    return {
        "service": "PLUTON",
        "status": "online",
        "phase": "1",
        "message": "PLUTON core API is running."
    }



@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "PLUTON",
        "phase": "1",
        "database": "ready",
        "frontend": "available"
    }



@app.get("/api/summary")
def summary():
    return {
        "project": "PLUTON",
        "stack": ["FastAPI", "PostgreSQL", "SQLAlchemy", "Alembic"],
        "modules": ["users", "sports", "leagues", "teams", "fixtures", "predictions"],
        "status": "operational"
    }
