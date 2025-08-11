from typing import TYPE_CHECKING, List
from datetime import datetime
from datetime import UTC
from sqlmodel import Field, Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .user_role_relation import UserRoleRelation
    from .role_permission_relation import RolePermissionRelation

class Role(BaseIntModel, table=True):
    name: str
    code: str
    description: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )

    users: List["UserRoleRelation"] = Relationship(back_populates="role")
    permissions: List["RolePermissionRelation"] = Relationship(back_populates="role")