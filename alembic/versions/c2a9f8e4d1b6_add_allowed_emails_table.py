"""add allowed_emails table

Revision ID: c2a9f8e4d1b6
Revises: 1ff5174113d5
Create Date: 2026-07-05 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a9f8e4d1b6'
down_revision: Union[str, Sequence[str], None] = '1ff5174113d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('allowed_emails',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_allowed_emails_id'), 'allowed_emails', ['id'], unique=False)
    op.create_index(op.f('ix_allowed_emails_email'), 'allowed_emails', ['email'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_allowed_emails_email'), table_name='allowed_emails')
    op.drop_index(op.f('ix_allowed_emails_id'), table_name='allowed_emails')
    op.drop_table('allowed_emails')
