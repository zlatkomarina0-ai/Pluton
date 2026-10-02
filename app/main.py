from fastapi import FastAPI

from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.pluton import router as pluton_router

app = FastAPI(title="PLUTON", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(pluton_router)


@app.get("/")
async def root():
    return {"message": "PLUTON API is running"}
