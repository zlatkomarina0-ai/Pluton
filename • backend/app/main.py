from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.pluton import router as pluton_router

app = FastAPI(
    title="PLUTON",
    version="1.0.0",
    description="PLUTON API Server"
)


@app.get("/")
def read_root():
    return {"message": "PLUTON API", "service": "PLUTON", "version": "1.0.0"}


@app.get("/ready")
def readiness_check():
    return {"ready": True, "service": "PLUTON"}


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(pluton_router)
