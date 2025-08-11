"""seed default admin user

Revision ID: a1b2c3d4e5f6
Revises: 67a4d860c757
Create Date: 2025-08-11 02:00:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime
from uuid import uuid4
import os

try:
    # Hashing for the seeded password
    from passlib.context import CryptContext
except Exception:  # pragma: no cover - in case passlib isn't available, we still create the row with plain password
    CryptContext = None  # type: ignore


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "67a4d860c757"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert a default admin user if it doesn't already exist.

    You can override defaults via environment variables before running migrations:
    - SEED_USER_EMAIL (default: admin@gmail.com)
    - SEED_USER_PASSWORD (default: password)
    - SEED_USER_NAME (default: Admin)
    - SEED_USER_LAST_NAME (default: User)
    - SEED_USER_PHONE (default: 0000000000)
    - SEED_USER_ADDRESS (default: N/A)
    """
    connection = op.get_bind()

    seed_email = os.getenv("SEED_USER_EMAIL", "admin@gmail.com").strip()
    seed_password = os.getenv("SEED_USER_PASSWORD", "password")
    seed_name = os.getenv("SEED_USER_NAME", "Admin").strip()
    seed_last_name = os.getenv("SEED_USER_LAST_NAME", "User").strip()
    seed_phone = os.getenv("SEED_USER_PHONE", "0000000000").strip()
    seed_address = os.getenv("SEED_USER_ADDRESS", "N/A").strip()

    # Hash the password if passlib is available, otherwise store as-is
    if CryptContext is not None:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(seed_password)
    else:
        hashed_password = seed_password

    user_id = uuid4()
    created_at = datetime.utcnow()
    token = uuid4().hex
    refresh_token = uuid4().hex

    # Insert only if email doesn't exist already
    insert_sql = sa.text(
        'INSERT INTO "user" (id, created_at, name, last_name, phone, address, email, password, token, refresh_token) '
        'SELECT :id, :created_at, :name, :last_name, :phone, :address, :email, :password, :token, :refresh_token '
        'WHERE NOT EXISTS (SELECT 1 FROM "user" WHERE email = :email)'
    )

    connection.execute(
        insert_sql,
        {
            "id": user_id,
            "created_at": created_at,
            "name": seed_name,
            "last_name": seed_last_name,
            "phone": seed_phone,
            "address": seed_address,
            "email": seed_email,
            "password": hashed_password,
            "token": token,
            "refresh_token": refresh_token,
        },
    )


def downgrade() -> None:
    """Remove the default admin user seeded in upgrade()."""
    connection = op.get_bind()
    seed_email = os.getenv("SEED_USER_EMAIL", "admin@gmail.com").strip()

    delete_sql = sa.text('DELETE FROM "user" WHERE email = :email')
    connection.execute(delete_sql, {"email": seed_email})


