"""assign_admin_role_to_admin_user

Revision ID: 1f02dc62ed2c
Revises: f6a7b8c9d0e1
Create Date: 2025-11-12 23:15:08.589838

"""
from typing import Sequence, Union
import os

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f02dc62ed2c'
down_revision: Union[str, Sequence[str], None] = 'f6a7b8c9d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Assign admin role to admin@guelp.com user."""
    connection = op.get_bind()
    
    # Use the same email as the seed user migration
    admin_email = os.getenv("SEED_USER_EMAIL", "admin@guelp.com").strip()
    
    # Get admin role ID
    role_row = connection.execute(
        sa.text("SELECT id FROM role WHERE code = 'admin'")
    )
    role_id = role_row.scalar()
    
    if role_id is None:
        # Create admin role if it doesn't exist
        connection.execute(
            sa.text(
                "INSERT INTO role (name, code, description, created_at) "
                "SELECT 'Administrator', 'admin', 'Administrator role', NOW() "
                "WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'admin')"
            )
        )
        role_row = connection.execute(
            sa.text("SELECT id FROM role WHERE code = 'admin'")
        )
        role_id = role_row.scalar()
    
    # Get user ID
    user_row = connection.execute(
        sa.text('SELECT id FROM "user" WHERE email = :email'),
        {"email": admin_email}
    )
    user_id = user_row.scalar()
    
    # Assign admin role to user
    if user_id is not None and role_id is not None:
        connection.execute(
            sa.text(
                "INSERT INTO user_role_relation (user_id, role_id, relation_type) "
                "SELECT :user_id, :role_id, 'direct' "
                "WHERE NOT EXISTS ("
                "  SELECT 1 FROM user_role_relation "
                "  WHERE user_id = :user_id AND role_id = :role_id"
                ")"
            ),
            {"user_id": user_id, "role_id": role_id},
        )


def downgrade() -> None:
    """Remove admin role from admin user."""
    connection = op.get_bind()
    admin_email = os.getenv("SEED_USER_EMAIL", "admin@guelp.com").strip()
    
    connection.execute(
        sa.text(
            "DELETE FROM user_role_relation "
            "WHERE user_id = (SELECT id FROM \"user\" WHERE email = :email) "
            "AND role_id = (SELECT id FROM role WHERE code = 'admin')"
        ),
        {"email": admin_email},
    )
