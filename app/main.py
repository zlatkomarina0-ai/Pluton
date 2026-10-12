from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="PLUTON Core", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class PredictionRequest(BaseModel):
    fixture_id: int
    home_score: int
    away_score: int
    note: str | None = None


@app.post("/api/predictions")
def create_prediction(payload: PredictionRequest):
    return {
        "status": "accepted",
        "fixture_id": payload.fixture_id,
        "prediction": {
            "home_score": payload.home_score,
            "away_score": payload.away_score,
            "note": payload.note,
        },
        "message": "Prediction accepted and queued for processing."
    }
