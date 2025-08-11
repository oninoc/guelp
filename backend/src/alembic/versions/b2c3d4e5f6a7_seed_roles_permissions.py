"""seed default roles and permissions and link to admin user

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2025-08-11 02:20:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    # Defaults
    admin_email = os.getenv("SEED_USER_EMAIL", "admin@gmail.com").strip()

    # Upsert roles
    roles = [
        {"name": "Administrator", "code": "admin", "description": "Administrator role"},
        {"name": "User", "code": "user", "description": "Standard user role"},
    ]
    for role in roles:
        connection.execute(
            sa.text(
                "INSERT INTO role (name, code, description, created_at)\n"
                "SELECT :name, :code, :description, NOW()\n"
                "WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = :code)"
            ),
            role,
        )

    # Upsert permissions
    permissions = [
        {"name": "Manage Users", "code": "manage_users", "description": "Create/Update/Delete users"},
        {"name": "Manage Roles", "code": "manage_roles", "description": "Assign/Create roles"},
        {"name": "Manage Permissions", "code": "manage_permissions", "description": "Assign/Create permissions"},
    ]
    for perm in permissions:
        connection.execute(
            sa.text(
                "INSERT INTO permission (name, code, description, created_at)\n"
                "SELECT :name, :code, :description, NOW()\n"
                "WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = :code)"
            ),
            perm,
        )

    # Link admin role to permissions
    # Fetch role id for admin
    role_row = connection.execute(sa.text("SELECT id FROM role WHERE code = 'admin'"))
    role_id = role_row.scalar()
    if role_id is not None:
        perm_ids = connection.execute(sa.text("SELECT id FROM permission WHERE code IN ('manage_users','manage_roles','manage_permissions')"))
        for pid in [row[0] for row in perm_ids.fetchall()]:
            connection.execute(
                sa.text(
                    "INSERT INTO role_permission_relation (role_id, permission_id, relation_type)\n"
                    "SELECT :role_id, :permission_id, 'direct'\n"
                    "WHERE NOT EXISTS (SELECT 1 FROM role_permission_relation WHERE role_id=:role_id AND permission_id=:permission_id)"
                ),
                {"role_id": role_id, "permission_id": pid},
            )

    # Link admin user to admin role
    user_row = connection.execute(sa.text('SELECT id FROM "user" WHERE email = :email'), {"email": admin_email})
    user_id = user_row.scalar()
    if user_id is not None and role_id is not None:
        connection.execute(
            sa.text(
                "INSERT INTO user_role_relation (user_id, role_id, relation_type)\n"
                "SELECT :user_id, :role_id, 'direct'\n"
                "WHERE NOT EXISTS (SELECT 1 FROM user_role_relation WHERE user_id=:user_id AND role_id=:role_id)"
            ),
            {"user_id": user_id, "role_id": role_id},
        )


def downgrade() -> None:
    connection = op.get_bind()
    admin_email = os.getenv("SEED_USER_EMAIL", "admin@gmail.com").strip()

    # Unlink admin user from admin role
    connection.execute(
        sa.text(
            "DELETE FROM user_role_relation WHERE user_id = (SELECT id FROM \"user\" WHERE email = :email)"
        ),
        {"email": admin_email},
    )

    # Remove role-permission links for admin role
    connection.execute(sa.text("DELETE FROM role_permission_relation WHERE role_id = (SELECT id FROM role WHERE code = 'admin')"))

    # Optionally keep roles/permissions, or remove them if you want a clean downgrade
    # Here we keep them.


