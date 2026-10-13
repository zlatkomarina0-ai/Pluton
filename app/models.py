import uuid
from sqlalchemy import (
    Column, String, Boolean, Date, DateTime, Integer, Text, ForeignKey, Numeric, JSON, UniqueConstraint
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
    is_archived = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    protected_from_auto_update = Column(Boolean, default=True, nullable=False)
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
    __table_args__ = (
        UniqueConstraint("sport_id", "external_id", name="uq_fixture_external_id_per_sport"),
        UniqueConstraint("sport_id", "event_id", name="uq_fixture_event_id_per_sport"),
    )

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    sport_id = Column(UUID(as_uuid=False), ForeignKey("sports.id"), nullable=False)
    league_id = Column(UUID(as_uuid=False), ForeignKey("leagues.id"), nullable=True)
    season_id = Column(UUID(as_uuid=False), ForeignKey("seasons.id"), nullable=True)
    external_id = Column(String(255), nullable=True)
    event_id = Column(String(255), nullable=True)
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
    sport = Column(String(50), nullable=False, default="football")
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    url = Column(Text, nullable=True)
    api_key_encrypted = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=100, nullable=False)
    status = Column(String(50), default="unknown", nullable=False)
    last_success_at = Column(DateTime(timezone=True), nullable=True)
    last_failure_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    logs = relationship("SourceLog", back_populates="source", cascade="all, delete-orphan")


class SourceLog(Base):
    __tablename__ = "source_logs"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    source_id = Column(UUID(as_uuid=False), ForeignKey("source_registry.id", ondelete="CASCADE"), nullable=False)
    sport_id = Column(UUID(as_uuid=False), ForeignKey("sports.id"), nullable=True)
    sport = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    response_status = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    source = relationship("SourceRegistry", back_populates="logs")

# rest of models kept as-is
