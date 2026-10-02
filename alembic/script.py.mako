"""Alelembic script template."""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "%(rev)s"
down_revision = "%(down_revision)s"
branch_labels = "%(branch_labels)s"
depends_on = "%(depends_on)s"


def upgrade() -> None:
    %(upgrades)s


def downgrade() -> None:
    %(downgrades)s
