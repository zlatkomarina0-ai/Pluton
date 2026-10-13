from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models import AuditLog


class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        *,
        entity_type: str,
        action: str,
        entity_id: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            details=details or {},
            created_at=datetime.utcnow(),
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def log_delete(db: Session, *, entity_type: str, entity_id: Optional[str], user_id: Optional[str] = None, reason: str = "manual_delete") -> AuditLog:
        return AuditService.log_event(
            db,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            action="delete",
            details={"reason": reason, "protected": True},
        )
