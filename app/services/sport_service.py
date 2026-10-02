from sqlalchemy.orm import Session

from app.models import Sport


class SportService:
    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Sport).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, code: str, name: str, active: bool = True):
        sport = Sport(code=code, name=name, active=active)
        db.add(sport)
        db.commit()
        db.refresh(sport)
        return sport
