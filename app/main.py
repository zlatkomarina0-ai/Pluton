from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.routers import analysis, auth, fixtures, health, predictions

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="PLUTON sports prediction API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(fixtures.router)
app.include_router(predictions.router)
app.include_router(analysis.router)


@app.get("/")
def root():
    return {"message": "PLUTON API is running"}


@app.get("/ready")
def readiness():
    return {"ready": True}
