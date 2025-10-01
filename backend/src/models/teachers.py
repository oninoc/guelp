from typing import TYPE_CHECKING, List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user import User
    from .classroom_subject import ClassroomSubject
    from .classrooms import Classroom
    from .qualifications import Qualification
    from .classes import Classes
    from .subjects import Subject


class Teacher(BaseUUIDModel, table=True):
    names: str
    father_last_name: str
    mother_last_name: str
    document_type: str
    document_number: str
    birth_date: str
    gender: str
    nationality: str
    user_id: UUID = Field(foreign_key="user.id")

    user: "User" = Relationship(
        back_populates="teacher", sa_relationship_kwargs={"uselist": False}
    )
    classroom_subjects: List["ClassroomSubject"] = Relationship(
        back_populates="teacher",
        sa_relationship_kwargs={"foreign_keys": "ClassroomSubject.teacher_id"},
    )
    substitute_classroom_subjects: List["ClassroomSubject"] = Relationship(
        back_populates="substitute_teacher",
        sa_relationship_kwargs={
            "foreign_keys": "ClassroomSubject.substitute_teacher_id"
        },
    )
    tutor_classrooms: List["Classroom"] = Relationship(back_populates="tutor")
    qualifications: List["Qualification"] = Relationship(back_populates="teacher")
    classes: List["Classes"] = Relationship(back_populates="teacher")

    @property
    def subjects(self) -> List["Subject"]:
        subjects: List["Subject"] = []
        for classroom_subject in self.classroom_subjects:
            if classroom_subject.subject and classroom_subject.subject not in subjects:
                subjects.append(classroom_subject.subject)
        return subjects