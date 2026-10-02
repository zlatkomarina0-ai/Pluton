from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User, Sport, League, Season, Team, Fixture, Prediction, AnalysisResult
from app.schemas import (
    UserCreate, UserRead,
    SportCreate, SportRead,
    LeagueCreate, LeagueRead,
    SeasonCreate, SeasonRead,
    TeamCreate, TeamRead,
    FixtureCreate, FixtureRead,
    PredictionCreate, PredictionRead,
    AnalysisResultCreate, AnalysisResultRead,
)

router = APIRouter(prefix="/api/v1", tags=["pluton"])


@router.get("/users", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/sports", response_model=List[SportRead])
def get_sports(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Sport).offset(skip).limit(limit).all()


@router.post("/sports", response_model=SportRead, status_code=status.HTTP_201_CREATED)
def create_sport(payload: SportCreate, db: Session = Depends(get_db)):
    sport = Sport(**payload.dict())
    db.add(sport)
    db.commit()
    db.refresh(sport)
    return sport


@router.get("/leagues", response_model=List[LeagueRead])
def get_leagues(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(League).offset(skip).limit(limit).all()


@router.post("/leagues", response_model=LeagueRead, status_code=status.HTTP_201_CREATED)
def create_league(payload: LeagueCreate, db: Session = Depends(get_db)):
    league = League(**payload.dict())
    db.add(league)
    db.commit()
    db.refresh(league)
    return league


@router.get("/seasons", response_model=List[SeasonRead])
def get_seasons(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Season).offset(skip).limit(limit).all()


@router.post("/seasons", response_model=SeasonRead, status_code=status.HTTP_201_CREATED)
def create_season(payload: SeasonCreate, db: Session = Depends(get_db)):
    season = Season(**payload.dict())
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


@router.get("/teams", response_model=List[TeamRead])
def get_teams(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Team).offset(skip).limit(limit).all()


@router.post("/teams", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    team = Team(**payload.dict())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get("/fixtures", response_model=List[FixtureRead])
def get_fixtures(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Fixture).offset(skip).limit(limit).all()


@router.post("/fixtures", response_model=FixtureRead, status_code=status.HTTP_201_CREATED)
def create_fixture(payload: FixtureCreate, db: Session = Depends(get_db)):
    fixture = Fixture(**payload.dict())
    db.add(fixture)
    db.commit()
    db.refresh(fixture)
    return fixture


@router.get("/predictions", response_model=List[PredictionRead])
def get_predictions(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Prediction).offset(skip).limit(limit).all()


@router.post("/predictions", response_model=PredictionRead, status_code=status.HTTP_201_CREATED)
def create_prediction(payload: PredictionCreate, db: Session = Depends(get_db)):
    prediction = Prediction(**payload.dict())
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/analysis-results", response_model=List[AnalysisResultRead])
def get_analysis_results(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(AnalysisResult).offset(skip).limit(limit).all()


@router.post("/analysis-results", response_model=AnalysisResultRead, status_code=status.HTTP_201_CREATED)
def create_analysis_result(payload: AnalysisResultCreate, db: Session = Depends(get_db)):
    analysis = AnalysisResult(**payload.dict())
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis
