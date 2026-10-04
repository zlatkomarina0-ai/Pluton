import os


class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
    JWT_SECRET = os.getenv("JWT_SECRET")
    if ENVIRONMENT == "production" and not JWT_SECRET:
        raise RuntimeError("JWT_SECRET must be set when ENVIRONMENT=production")
    JWT_SECRET = JWT_SECRET or "dev-secret-change-in-production"
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
    APP_NAME = os.getenv("APP_NAME", "PLUTON")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pluton")
    CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]


settings = Settings()
