from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_role_relation import UserRoleRelation

class User(BaseUUIDModel, table=True):
    name: str
    last_name: str
    phone: str
    address: str
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    token: str = Field(nullable=False)
    refresh_token: str = Field(nullable=False)

    roles: List["UserRoleRelation"] = Relationship(back_populates="user")