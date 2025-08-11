from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

from .base.base_model import BaseModel

if TYPE_CHECKING:
    from .role import Role
    from .permission import Permission

class RolePermissionRelation(BaseModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)
    relation_type: str

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")
