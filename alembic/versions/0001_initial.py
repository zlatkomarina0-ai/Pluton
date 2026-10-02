"""Initial database schema migration.

Revision ID: 0001_initial
Creates all base tables for PLUTON Phase 1 and Phase 2.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema"""
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("username", sa.String(100), nullable=False, unique=True),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("password_hash", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create roles table
    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create user_roles table
    op.create_table(
        "user_roles",
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )

    # Create sports table
    op.create_table(
        "sports",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create leagues table
    op.create_table(
        "leagues",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("sport_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("code", sa.String(100), nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("country", sa.String(255), nullable=True),
        sa.Column("is_international", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["sport_id"], ["sports.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create seasons table
    op.create_table(
        "seasons",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("league_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["league_id"], ["leagues.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create teams table
    op.create_table(
        "teams",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("sport_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("external_id", sa.String(255), nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("short_name", sa.String(100), nullable=True),
        sa.Column("country", sa.String(255), nullable=True),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["sport_id"], ["sports.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create fixtures table
    op.create_table(
        "fixtures",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("sport_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("league_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("season_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("external_id", sa.String(255), nullable=True),
        sa.Column("home_team_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("away_team_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("kickoff_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="scheduled"),
        sa.Column("venue", sa.String(255), nullable=True),
        sa.Column("round_name", sa.String(255), nullable=True),
        sa.Column("competition_name", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["sport_id"], ["sports.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["league_id"], ["leagues.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["home_team_id"], ["teams.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["away_team_id"], ["teams.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create source_registry table
    op.create_table(
        "source_registry",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("sport_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(100), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("api_key_encrypted", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["sport_id"], ["sports.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create fixture_source_data table
    op.create_table(
        "fixture_source_data",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("fixture_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("payload", postgresql.JSON(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("quality_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["fixture_id"], ["fixtures.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_id"], ["source_registry.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create source_quality table
    op.create_table(
        "source_quality",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("fixture_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("quality_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("checked_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["source_registry.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["fixture_id"], ["fixtures.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create predictions table
    op.create_table(
        "predictions",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("fixture_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("prediction_type", sa.String(100), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("market_type", sa.String(100), nullable=True),
        sa.Column("confidence", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("strength", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["fixture_id"], ["fixtures.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create prediction_history table
    op.create_table(
        "prediction_history",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("prediction_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("old_value", postgresql.JSON(), nullable=True),
        sa.Column("new_value", postgresql.JSON(), nullable=True),
        sa.Column("changed_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["prediction_id"], ["predictions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["changed_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create analysis_results table
    op.create_table(
        "analysis_results",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("fixture_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("source_summary", postgresql.JSON(), nullable=True),
        sa.Column("consensus_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("weighted_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("pluton_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("confidence_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("result_label", sa.String(100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["fixture_id"], ["fixtures.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create performance_summary table
    op.create_table(
        "performance_summary",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("sport_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("league_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("season_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("metric_name", sa.String(150), nullable=False),
        sa.Column("metric_value", sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column("period_start", sa.Date(), nullable=True),
        sa.Column("period_end", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["sport_id"], ["sports.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["league_id"], ["leagues.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create result_events table
    op.create_table(
        "result_events",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("fixture_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("prediction_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("outcome", sa.String(50), nullable=False),
        sa.Column("actual_home_score", sa.Integer(), nullable=True),
        sa.Column("actual_away_score", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["fixture_id"], ["fixtures.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["prediction_id"], ["predictions.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create audit_logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("details", postgresql.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for common queries
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_fixtures_sport_id", "fixtures", ["sport_id"])
    op.create_index("ix_fixtures_league_id", "fixtures", ["league_id"])
    op.create_index("ix_fixtures_season_id", "fixtures", ["season_id"])
    op.create_index("ix_fixtures_status", "fixtures", ["status"])
    op.create_index("ix_predictions_fixture_id", "predictions", ["fixture_id"])
    op.create_index("ix_predictions_user_id", "predictions", ["user_id"])
    op.create_index("ix_analysis_results_fixture_id", "analysis_results", ["fixture_id"])
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_entity_id", "audit_logs", ["entity_id"])


def downgrade() -> None:
    """Downgrade schema"""
    # Drop all tables in reverse order
    op.drop_table("audit_logs")
    op.drop_table("result_events")
    op.drop_table("performance_summary")
    op.drop_table("analysis_results")
    op.drop_table("prediction_history")
    op.drop_table("predictions")
    op.drop_table("source_quality")
    op.drop_table("fixture_source_data")
    op.drop_table("source_registry")
    op.drop_table("fixtures")
    op.drop_table("teams")
    op.drop_table("seasons")
    op.drop_table("leagues")
    op.drop_table("sports")
    op.drop_table("user_roles")
    op.drop_table("roles")
    op.drop_table("users")
