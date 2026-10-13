import uuid
from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import Date, UniqueConstraint
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import ApiQuota


class ApiQuotaService:
    @staticmethod
    def _key_for_request(request) -> str:
        return getattr(request.state, "client_id", request.client.host if request.client else "unknown")

    @staticmethod
    def _today() -> date:
        return datetime.utcnow().date()

    @classmethod
    def allow_request(cls, request, limit: int = 100) -> bool:
        db: Session = SessionLocal()
        try:
            key = cls._key_for_request(request)
            today = cls._today()

            quota = db.query(ApiQuota).filter(ApiQuota.key == key, ApiQuota.date == today).first()
            if quota is None:
                quota = ApiQuota(key=key, date=today, count=1)
                db.add(quota)
                db.commit()
                return True

            if quota.count >= limit:
                return False

            quota.count += 1
            quota.updated_at = datetime.utcnow()
            db.add(quota)
            db.commit()
            return True
        finally:
            db.close()

    @classmethod
    def reset_expired(cls, db: Session) -> None:
        today = cls._today()
        db.query(ApiQuota).filter(ApiQuota.date < today).delete()
        db.commit()
