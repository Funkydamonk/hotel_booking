"""Fixed the password insert issue

Revision ID: aaee3824a204
Revises: c3b4e4158aa8
Create Date: 2025-03-26 22:42:58.544998

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aaee3824a204"
down_revision: Union[str, None] = "c3b4e4158aa8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=70), nullable=False)
    )
    op.drop_column("users", "password")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(length=70), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "hashed_password")
