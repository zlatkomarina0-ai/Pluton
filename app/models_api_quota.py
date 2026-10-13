from sqlalchemy import Column, Date, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class ApiQuota(Base):
    __tablename__ = "api_quota"
    __table_args__ = (
        UniqueConstraint("key", "date", name="uq_api_quota_key_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), nullable=False)
    date = Column(Date, nullable=False, default=func.current_date())
    count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


__all__ = ["ApiQuota"]
