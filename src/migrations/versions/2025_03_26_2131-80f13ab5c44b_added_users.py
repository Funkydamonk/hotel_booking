"""Added users

Revision ID: 80f13ab5c44b
Revises: 61b4c64d500f
Create Date: 2025-03-26 21:31:57.580033

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "80f13ab5c44b"
down_revision: Union[str, None] = "61b4c64d500f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("passwowrd", sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
