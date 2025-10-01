from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_role_relation import UserRoleRelation
    from .teachers import Teacher
    from .students import Student


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
    teacher: Optional["Teacher"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    student: Optional["Student"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )