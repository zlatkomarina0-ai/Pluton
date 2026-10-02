from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.pluton import router as pluton_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="PLUTON: Sports Analytics & Prediction Engine",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if "*" not in settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(pluton_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PLUTON API is running",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }
