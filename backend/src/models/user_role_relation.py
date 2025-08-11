from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_model import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .role import Role

class UserRoleRelation(BaseModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    relation_type: str

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")