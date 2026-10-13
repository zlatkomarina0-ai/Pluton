import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "PLUTON")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pluton")

    ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"
    SCHEDULER_INTERVAL_SECONDS = int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "60"))
    API_QUOTA_LIMIT_PER_DAY = int(os.getenv("API_QUOTA_LIMIT_PER_DAY", "100"))
    API_QUOTA_RESET_HOUR_UTC = int(os.getenv("API_QUOTA_RESET_HOUR_UTC", "0"))

    PROVIDER_TIMEOUT_SECONDS = int(os.getenv("PROVIDER_TIMEOUT_SECONDS", "5"))
    PROVIDER_MAX_RETRIES = int(os.getenv("PROVIDER_MAX_RETRIES", "2"))
    PROVIDER_BACKOFF_BASE_SECONDS = float(os.getenv("PROVIDER_BACKOFF_BASE_SECONDS", "0.25"))
    PROVIDER_RATE_LIMIT_PER_MINUTE = int(os.getenv("PROVIDER_RATE_LIMIT_PER_MINUTE", "60"))


settings = Settings()
