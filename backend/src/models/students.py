from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user import User


class Student(BaseUUIDModel, table=True):
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    phone: str
    address: str
    email: str
    degree: str
    level: str
    classroom: str
    birth_date: str
    gender: str
    nationality: str
    document_type: str
    document_number: str
    responsible_name: str
    responsible_phone: str
    responsible_email: str
    responsible_address: str
    user_id: str = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="student")

    @property
    def full_name(self):
        return f"{self.names} {self.father_last_name} {self.mother_last_name}"
    
    @property
    def full_level(self):
        return f"{self.degree} - {self.level}"