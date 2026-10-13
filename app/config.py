import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "PLUTON")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pluton")

    PROVIDER_TIMEOUT_SECONDS = int(os.getenv("PROVIDER_TIMEOUT_SECONDS", "5"))
    PROVIDER_MAX_RETRIES = int(os.getenv("PROVIDER_MAX_RETRIES", "2"))
    PROVIDER_BACKOFF_BASE_SECONDS = float(os.getenv("PROVIDER_BACKOFF_BASE_SECONDS", "0.25"))
    PROVIDER_RATE_LIMIT_PER_MINUTE = int(os.getenv("PROVIDER_RATE_LIMIT_PER_MINUTE", "60"))


settings = Settings()
