"""Created m2m table and facilities for rooms

Revision ID: 965b871db95c
Revises: 9a09fe6d7c2b
Create Date: 2025-04-01 21:25:22.190313

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "965b871db95c"
down_revision: Union[str, None] = "9a09fe6d7c2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
