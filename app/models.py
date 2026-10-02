import uuid
from sqlalchemy import (
    Column, String, Boolean, Date, DateTime, Integer, Text, ForeignKey, Numeric, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    predictions = relationship("Prediction", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(UUID(as_uuid=False), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Sport(Base):
    __tablename__ = "sports"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class League(Base):
    __tablename__ = "leagues"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    sport_id = Column(UUID(as_uuid=False), ForeignKey("sports.id"), nullable=False)
    code = Column(String(100), nullable=True)
    name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=True)
    is_international = Column(Boolean, default=False, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Season(Base):
    __tablename__ = "seasons"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    league_id = Column(UUID(as_uuid=False), ForeignKey("leagues.id"), nullable=False)
    name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    sport_id = Column(UUID(as_uuid=False), ForeignKey("sports.id"), nullable=False)
    external_id = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(100), nullable=True)
    country = Column(String(255), nullable=True)
    logo_url = Column(Text, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Fixture(Base):
    __tablename__ = "fixtures"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    sport_id = Column(UUID(as_uuid=False), ForeignKey("sports.id"), nullable=False)
    league_id = Column(UUID(as_uuid=False), ForeignKey("leagues.id"), nullable=True)
    season_id = Column(UUID(as_uuid=False), ForeignKey("seasons.id"), nullable=True)
    external_id = Column(String(255), nullable=True)
    home_team_id = Column(UUID(as_uuid=False), ForeignKey("teams.id"), nullable=True)
    away_team_id = Column(UUID(as_uuid=False), ForeignKey("teams.id"), nullable=True)
    kickoff_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="scheduled", nullable=False)
    venue = Column(String(255), nullable=True)
    round_name = Column(String(255), nullable=True)
    competition_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SourceRegistry(Base):
    __tablename__ = "source_registry"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    sport_id = Column(UUID(as_uuid=False), ForeignKey("sports.id"), nullable=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    url = Column(Text, nullable=True)
    api_key_encrypted = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=100, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class FixtureSourceData(Base):
    __tablename__ = "fixture_source_data"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    fixture_id = Column(UUID(as_uuid=False), ForeignKey("fixtures.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(UUID(as_uuid=False), ForeignKey("source_registry.id"), nullable=False)
    payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    quality_score = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class SourceQuality(Base):
    __tablename__ = "source_quality"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    source_id = Column(UUID(as_uuid=False), ForeignKey("source_registry.id"), nullable=False)
    fixture_id = Column(UUID(as_uuid=False), ForeignKey("fixtures.id"), nullable=True)
    status = Column(String(50), nullable=False)
    error_message = Column(Text, nullable=True)
    quality_score = Column(Numeric(5, 2), nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    fixture_id = Column(UUID(as_uuid=False), ForeignKey("fixtures.id"), nullable=False)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    prediction_type = Column(String(100), nullable=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    market_type = Column(String(100), nullable=True)
    confidence = Column(Numeric(5, 2), nullable=True)
    strength = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="predictions")


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    prediction_id = Column(UUID(as_uuid=False), ForeignKey("predictions.id"), nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    changed_by = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    fixture_id = Column(UUID(as_uuid=False), ForeignKey("fixtures.id"), nullable=False)
    source_summary = Column(JSON, nullable=True)
    consensus_score = Column(Numeric(5, 2), nullable=True)
    weighted_score = Column(Numeric(5, 2), nullable=True)
    pluton_score = Column(Numeric(5, 2), nullable=True)
    confidence_score = Column(Numeric(5, 2), nullable=True)
    result_label = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PerformanceSummary(Base):
    __tablename__ = "performance_summary"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    sport_id = Column(UUID(as_uuid=False), ForeignKey("sports.id"), nullable=True)
    league_id = Column(UUID(as_uuid=False), ForeignKey("leagues.id"), nullable=True)
    season_id = Column(UUID(as_uuid=False), ForeignKey("seasons.id"), nullable=True)
    metric_name = Column(String(150), nullable=False)
    metric_value = Column(Numeric(10, 4), nullable=True)
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ResultEvent(Base):
    __tablename__ = "result_events"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    fixture_id = Column(UUID(as_uuid=False), ForeignKey("fixtures.id"), nullable=False)
    prediction_id = Column(UUID(as_uuid=False), ForeignKey("predictions.id"), nullable=True)
    outcome = Column(String(50), nullable=False)
    actual_home_score = Column(Integer, nullable=True)
    actual_away_score = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(UUID(as_uuid=False), nullable=True)
    action = Column(String(100), nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
