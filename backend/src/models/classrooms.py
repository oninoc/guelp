from typing import TYPE_CHECKING, List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .teachers import Teacher
    from .classroom_subject import ClassroomSubject
    from .classes import Classes


class Classroom(BaseUUIDModel, table=True):
    description: str
    level: str
    degree: str
    start_time: Optional[str] = None    
    end_time: Optional[str] = None
    tutor_id: Optional[UUID] = Field(foreign_key="teacher.id")

    tutor: Optional["Teacher"] = Relationship(
        back_populates="tutor_classrooms",
        sa_relationship_kwargs={"foreign_keys": "Classroom.tutor_id", "uselist": False},
    )
    classroom_subjects: List["ClassroomSubject"] = Relationship(
        back_populates="classroom"
    )
    classes: List["Classes"] = Relationship(back_populates="classroom")

    @property
    def subjects(self):
        subjects = []
        for relation in self.classroom_subjects:
            if relation.subject and relation.subject not in subjects:
                subjects.append(relation.subject)
        return subjects
