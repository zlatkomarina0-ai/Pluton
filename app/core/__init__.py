import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App
    APP_NAME = os.getenv("APP_NAME", "PLUTON")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Database
    USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() in {"1", "true", "yes", "y"}
    DATABASE_URL = os.getenv("DATABASE_URL") or (
        "sqlite:///./pluton.db"
        if os.getenv("USE_SQLITE", "true").lower() in {"1", "true", "yes", "y"}
        else "postgresql://postgres:postgres@localhost:5432/pluton"
    )

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production-secret-key-256-bits")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

    # CORS
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
        if origin.strip()
    ]

    # Security
    DEBUG = ENVIRONMENT == "development"
    TESTING = ENVIRONMENT == "testing"


settings = Settings()
