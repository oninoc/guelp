from typing import TYPE_CHECKING, List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .files import Files
    from .classrooms import Classroom
    from .teachers import Teacher
    from .subjects import Subject
    from .classroom_subject import ClassroomSubject


class Classes(BaseIntModel, table=True):
    classroom_id: UUID = Field(foreign_key="classroom.id")
    subject_id: int = Field(foreign_key="subject.id")
    teacher_id: UUID = Field(foreign_key="teacher.id")
    classroom_subject_id: Optional[int] = Field(
        default=None, foreign_key="classroom_subject.id"
    )

    classroom: "Classroom" = Relationship(back_populates="classes")
    subject: "Subject" = Relationship(back_populates="classes")
    teacher: "Teacher" = Relationship(back_populates="classes")
    classroom_subject: Optional["ClassroomSubject"] = Relationship(
        back_populates="classes"
    )
    files: List["Files"] = Relationship(back_populates="class_session")

    @property
    def documents(self) -> List["Files"]:
        from .files import FileType

        return [
            file
            for file in self.files
            if file.type
            in {
                FileType.PDF,
                FileType.WORD,
                FileType.EXCEL,
                FileType.POWERPOINT,
            }
        ]

    @property
    def videos(self) -> List["Files"]:
        from .files import FileType

        return [file for file in self.files if file.type == FileType.VIDEO]
