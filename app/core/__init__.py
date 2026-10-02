from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    JWT_SECRET = "PLUTON_DEV_SECRET"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRES_MINUTES = 60


settings = Settings()
