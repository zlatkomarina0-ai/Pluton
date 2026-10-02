from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Sport
from app.schemas import SportCreate, SportRead

router = APIRouter(prefix="/api/v1", tags=["sports"])


@router.get("/sports", response_model=List[SportRead])
def get_sports(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Sport).offset(skip).limit(limit).all()


@router.get("/sports/{sport_id}", response_model=SportRead)
def get_sport(sport_id: str, db: Session = Depends(get_db)):
    sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if not sport:
        raise HTTPException(status_code=404, detail="Sport not found")
    return sport


@router.post("/sports", response_model=SportRead, status_code=status.HTTP_201_CREATED)
def create_sport(payload: SportCreate, db: Session = Depends(get_db)):
    existing = db.query(Sport).filter(Sport.code == payload.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Sport code already exists")

    sport = Sport(**payload.dict())
    db.add(sport)
    db.commit()
    db.refresh(sport)
    return sport
