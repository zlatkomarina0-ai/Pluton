import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App
    APP_NAME = os.getenv("APP_NAME", "PLUTON")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

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

    # Security / runtime
    DEBUG = ENVIRONMENT == "development"
    TESTING = ENVIRONMENT == "testing"

    @classmethod
    def validate(cls):
        if cls.ENVIRONMENT == "production":
            if cls.JWT_SECRET in {"change-me-in-production-secret-key-256-bits", "dev-secret-change-in-production"}:
                raise RuntimeError("JWT_SECRET must be set to a secure secret in production.")
            if not cls.CORS_ORIGINS or cls.CORS_ORIGINS == ["*"]:
                raise RuntimeError("CORS_ORIGINS must be set explicitly in production.")


settings = Settings()
settings.validate()
