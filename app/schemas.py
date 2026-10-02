from typing import Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password_hash: Optional[str] = None


class UserRead(UserBase):
    id: str
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class SportBase(BaseModel):
    code: str
    name: str
    active: bool = True


class SportCreate(SportBase):
    pass


class SportRead(SportBase):
    id: str
    created_at: Optional[str] = None

    class Config:
        orm_mode = True


class LeagueBase(BaseModel):
    sport_id: str
    code: Optional[str] = None
    name: str
    country: Optional[str] = None
    is_international: bool = False
    active: bool = True


class LeagueCreate(LeagueBase):
    pass


class LeagueRead(LeagueBase):
    id: str
    created_at: Optional[str] = None

    class Config:
        orm_mode = True


class SeasonBase(BaseModel):
    league_id: str
    name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    active: bool = True


class SeasonCreate(SeasonBase):
    pass


class SeasonRead(SeasonBase):
    id: str
    created_at: Optional[str] = None

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    sport_id: str
    external_id: Optional[str] = None
    name: str
    short_name: Optional[str] = None
    country: Optional[str] = None
    logo_url: Optional[str] = None
    active: bool = True


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class FixtureBase(BaseModel):
    sport_id: str
    league_id: Optional[str] = None
    season_id: Optional[str] = None
    external_id: Optional[str] = None
    home_team_id: Optional[str] = None
    away_team_id: Optional[str] = None
    kickoff_at: Optional[str] = None
    status: str = "scheduled"
    venue: Optional[str] = None
    round_name: Optional[str] = None
    competition_name: Optional[str] = None


class FixtureCreate(FixtureBase):
    pass


class FixtureRead(FixtureBase):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class PredictionBase(BaseModel):
    fixture_id: str
    user_id: Optional[str] = None
    prediction_type: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    market_type: Optional[str] = None
    confidence: Optional[float] = None
    strength: Optional[float] = None


class PredictionCreate(PredictionBase):
    pass


class PredictionRead(PredictionBase):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class AnalysisResultBase(BaseModel):
    fixture_id: str
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
    id: str
    created_at: Optional[str] = None

    class Config:
        orm_mode = True
