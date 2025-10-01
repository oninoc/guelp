from typing import TYPE_CHECKING, List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user import User
    from .classroom_subject_student import ClassroomSubjectStudent

class Student(BaseUUIDModel, table=True):
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    responsible_name: Optional[str] = None
    responsible_phone: Optional[str] = None
    responsible_email: Optional[str] = None
    responsible_address: Optional[str] = None
    user_id: UUID = Field(foreign_key="user.id")

    user: "User" = Relationship(
        back_populates="student", sa_relationship_kwargs={"uselist": False}
    )
    classroom_subject_students: List["ClassroomSubjectStudent"] = Relationship(
        back_populates="student"
    )

    @property
    def full_name(self):
        return f"{self.names} {self.father_last_name} {self.mother_last_name}"