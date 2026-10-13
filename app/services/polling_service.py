import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models import SourceLog, SourceRegistry
from app.services.provider_client import ProviderClient


class PollingService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = ProviderClient()

    def _save_log(self, source: SourceRegistry, status: str, payload: Optional[Any] = None, error_message: Optional[str] = None, response_status: Optional[int] = None, duration_ms: Optional[int] = None) -> SourceLog:
        log = SourceLog(
            source_id=source.id,
            sport_id=source.sport_id,
            sport=source.sport,
            status=status,
            payload=payload,
            error_message=error_message,
            response_status=response_status,
            duration_ms=duration_ms,
        )
        self.db.add(log)
        return log

    def _update_source_state(self, source: SourceRegistry, success: bool) -> None:
        now = datetime.now(timezone.utc)
        source.status = "active" if success else "down"
        if success:
            source.last_success_at = now
        else:
            source.last_failure_at = now
        self.db.add(source)

    def poll_source(self, source: SourceRegistry) -> Dict[str, Any]:
        started_at = time.monotonic()
        payload = None
        error_message = None
        response_status = None
        status = "success"

        try:
            payload, response_status = self.provider.fetch_json(source.url)
        except Exception as exc:
            status = "failed"
            error_message = str(exc)

        duration_ms = int((time.monotonic() - started_at) * 1000)

        log = self._save_log(
            source=source,
            status=status,
            payload=payload,
            error_message=error_message,
            response_status=response_status,
            duration_ms=duration_ms,
        )

        self._update_source_state(source, status == "success")
        self.db.add(log)
        self.db.commit()

        return {
            "source_id": str(source.id),
            "source_name": source.name,
            "sport": source.sport,
            "status": status,
            "response_status": response_status,
            "duration_ms": duration_ms,
            "payload": payload,
            "error_message": error_message,
        }

    def poll_sport(self, sport: str, source_id: Optional[str] = None) -> Dict[str, Any]:
        query = self.db.query(SourceRegistry).filter(
            SourceRegistry.is_active.is_(True),
        )

        if source_id:
            query = query.filter(SourceRegistry.id == source_id)
        else:
            query = query.filter((SourceRegistry.sport == sport) | (SourceRegistry.sport_id == sport))

        sources: List[SourceRegistry] = query.order_by(SourceRegistry.priority.asc()).all()
        results = [self.poll_source(source) for source in sources]

        success_count = sum(1 for item in results if item["status"] == "success")
        failure_count = sum(1 for item in results if item["status"] == "failed")

        return {
            "sport": sport,
            "processed_sources": len(results),
            "success_count": success_count,
            "failure_count": failure_count,
            "results": results,
        }
