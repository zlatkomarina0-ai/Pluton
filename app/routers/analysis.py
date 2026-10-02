from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.dependencies import get_db
from app.schemas import PredictionCreate, PredictionRead
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/api/v1", tags=["predictions"])


@router.get("/predictions", response_model=List[PredictionRead])
def get_predictions(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return PredictionService.list(db, skip=skip, limit=limit)


@router.get("/predictions/me", response_model=List[PredictionRead])
def get_my_predictions(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return PredictionService.list_for_user(db, current_user_id, skip=skip, limit=limit)


@router.post("/predictions", response_model=PredictionRead, status_code=status.HTTP_201_CREATED)
def create_prediction(
    payload: PredictionCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    try:
        prediction = PredictionService.create(
            db,
            fixture_id=payload.fixture_id,
            user_id=current_user_id,
            prediction_type=payload.prediction_type,
            home_score=payload.home_score,
            away_score=payload.away_score,
            market_type=payload.market_type,
            confidence=payload.confidence,
            strength=payload.strength,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return prediction
