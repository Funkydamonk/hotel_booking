"""Increased password field char capacity

Revision ID: c3b4e4158aa8
Revises: 6253fc850336
Create Date: 2025-03-26 22:33:34.967921

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3b4e4158aa8"
down_revision: Union[str, None] = "6253fc850336"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "password",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(length=70),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
    )
