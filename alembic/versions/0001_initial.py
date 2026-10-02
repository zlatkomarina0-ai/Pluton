from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.analysis import router as analysis_router
from app.routers.auth import router as auth_router
from app.routers.fixtures import router as fixtures_router
from app.routers.health import router as health_router
from app.routers.pluton import router as pluton_router
from app.routers.predictions import router as predictions_router

app = FastAPI(title="PLUTON", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(pluton_router)
app.include_router(fixtures_router)
app.include_router(predictions_router)
app.include_router(analysis_router)


@app.get("/")
async def root():
    return {"message": "PLUTON API is running"}
