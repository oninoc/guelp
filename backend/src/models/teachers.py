from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user import User


class Teacher(BaseUUIDModel, table=True):
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    document_type: str
    document_number: str
    birth_date: str
    gender: str
    nationality: str
    principal_subject: str
    secondary_subject: str
    start_time: str
    end_time: str
    user_id: str = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="teacher")