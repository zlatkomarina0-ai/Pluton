from typing import Optional
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password_hash: Optional[str] = None


class UserRead(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SportBase(BaseModel):
    code: str
    name: str
    active: bool = True


class SportCreate(SportBase):
    pass


class SportRead(SportBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class LeagueBase(BaseModel):
    sport_id: UUID
    code: Optional[str] = None
    name: str
    country: Optional[str] = None
    is_international: bool = False
    active: bool = True


class LeagueCreate(LeagueBase):
    pass


class LeagueRead(LeagueBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class SeasonBase(BaseModel):
    league_id: UUID
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    active: bool = True


class SeasonCreate(SeasonBase):
    pass


class SeasonRead(SeasonBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    sport_id: UUID
    external_id: Optional[str] = None
    name: str
    short_name: Optional[str] = None
    country: Optional[str] = None
    logo_url: Optional[str] = None
    active: bool = True


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FixtureBase(BaseModel):
    sport_id: UUID
    league_id: Optional[UUID] = None
    season_id: Optional[UUID] = None
    external_id: Optional[str] = None
    home_team_id: Optional[UUID] = None
    away_team_id: Optional[UUID] = None
    kickoff_at: Optional[datetime] = None
    status: str = "scheduled"
    venue: Optional[str] = None
    round_name: Optional[str] = None
    competition_name: Optional[str] = None


class FixtureCreate(FixtureBase):
    pass


class FixtureRead(FixtureBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PredictionBase(BaseModel):
    fixture_id: UUID
    user_id: Optional[UUID] = None
    prediction_type: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    market_type: Optional[str] = None
    confidence: Optional[float] = None
    strength: Optional[float] = None


class PredictionCreate(PredictionBase):
    pass


class PredictionRead(PredictionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AnalysisResultBase(BaseModel):
    fixture_id: UUID
    source_summary: Optional[dict] = None
    consensus_score: Optional[float] = None
    weighted_score: Optional[float] = None
    pluton_score: Optional[float] = None
    confidence_score: Optional[float] = None
    result_label: Optional[str] = None
    notes: Optional[str] = None


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultRead(AnalysisResultBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
