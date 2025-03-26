"""Fixed users model

Revision ID: 6253fc850336
Revises: 80f13ab5c44b
Create Date: 2025-03-26 22:31:50.828676

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6253fc850336"
down_revision: Union[str, None] = "80f13ab5c44b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("password", sa.String(length=30), nullable=False))
    op.drop_column("users", "passwowrd")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "passwowrd", sa.VARCHAR(length=30), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "password")
