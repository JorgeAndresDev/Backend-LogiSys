"""make firebase_uid nullable

Revision ID: f7a8b9c0d1e2
Revises: e4d5f6b7a8c9
Create Date: 2026-07-06 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7a8b9c0d1e2'
down_revision: Union[str, Sequence[str], None] = 'e4d5f6b7a8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'firebase_uid',
                    existing_type=sa.String(),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('users', 'firebase_uid',
                    existing_type=sa.String(),
                    nullable=False)
