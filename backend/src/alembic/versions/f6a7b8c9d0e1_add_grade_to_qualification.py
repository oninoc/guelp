"""add grade column to qualification records

Revision ID: f6a7b8c9d0e1
Revises: e5f6a9b0c2d3
Create Date: 2025-11-12 20:10:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, Sequence[str], None] = "e5f6a9b0c2d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("qualification", sa.Column("grade", sa.String(length=4), nullable=True))


def downgrade() -> None:
    op.drop_column("qualification", "grade")

