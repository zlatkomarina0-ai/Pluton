import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "PLUTON")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() in {"1", "true", "yes", "y"}
    DATABASE_URL = os.getenv("DATABASE_URL") or (
        "sqlite:///./pluton.db" if os.getenv("USE_SQLITE", "true").lower() in {"1", "true", "yes", "y"} else "postgresql://postgres:postgres@localhost:5432/pluton"
    )


settings = Settings()
