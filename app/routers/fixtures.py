from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import FixtureCreate, FixtureRead
from app.services.fixtures_service import FixturesService

router = APIRouter(prefix="/api/v1", tags=["fixtures"])


@router.get("/fixtures", response_model=List[FixtureRead])
def get_fixtures(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return FixturesService.list(db, skip=skip, limit=limit)


@router.get("/fixtures/{fixture_id}", response_model=FixtureRead)
def get_fixture(fixture_id: str, db: Session = Depends(get_db)):
    fixture = FixturesService.get_by_id(db, fixture_id)
    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")
    return fixture


@router.post("/fixtures", response_model=FixtureRead, status_code=status.HTTP_201_CREATED)
def create_fixture(payload: FixtureCreate, db: Session = Depends(get_db)):
    try:
        return FixturesService.create(
            db,
            sport_id=payload.sport_id,
            league_id=payload.league_id,
            season_id=payload.season_id,
            home_team_id=payload.home_team_id,
            away_team_id=payload.away_team_id,
            status=payload.status,
            venue=payload.venue,
            round_name=payload.round_name,
            competition_name=payload.competition_name,
            external_id=payload.external_id,
            kickoff_at=payload.kickoff_at,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
