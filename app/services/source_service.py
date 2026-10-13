from typing import Optional

from sqlalchemy.orm import Session

from app.models import SourceRegistry


def get_sources(db: Session, sport: Optional[str] = None):
    query = db.query(SourceRegistry)
    if sport:
        query = query.filter(SourceRegistry.sport == sport)
    return query.order_by(SourceRegistry.priority.asc()).all()


def get_source(db: Session, source_id: str):
    return db.query(SourceRegistry).filter(SourceRegistry.id == source_id).first()


def create_source(db: Session, payload: dict) -> SourceRegistry:
    source = SourceRegistry(
        sport_id=payload.get("sport_id"),
        sport=payload.get("sport", "football"),
        name=payload["name"],
        type=payload.get("type", "api"),
        url=payload.get("url"),
        api_key_encrypted=payload.get("api_key_encrypted"),
        is_active=payload.get("is_active", True),
        priority=payload.get("priority", 100),
        status=payload.get("status", "unknown"),
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def update_source(db: Session, source: SourceRegistry, payload: dict) -> SourceRegistry:
    for field in ["sport_id", "sport", "name", "type", "url", "is_active", "priority", "status", "api_key_encrypted"]:
        if field in payload:
            setattr(source, field, payload[field])

    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def delete_source(db: Session, source: SourceRegistry) -> None:
    db.delete(source)
    db.commit()
