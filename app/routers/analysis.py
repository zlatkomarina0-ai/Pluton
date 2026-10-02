from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import AnalysisResultCreate, AnalysisResultRead
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.get("/analysis-results", response_model=List[AnalysisResultRead])
def get_analysis_results(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return AnalysisService.list(db, skip=skip, limit=limit)


@router.post("/analysis-results", response_model=AnalysisResultRead, status_code=status.HTTP_201_CREATED)
def create_analysis_result(payload: AnalysisResultCreate, db: Session = Depends(get_db)):
    try:
        result = AnalysisService.analyze_fixture(db, payload.fixture_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result
