from sqlalchemy.ext.asyncio import AsyncSession

from .repositories.user_repository import UserRepository
from .repositories.role_repository import RoleRepository
from .repositories.permission_repository import PermissionRepository
from .repositories.user_role_relation_repository import (
    UserRoleRelationRepository,
)
from .repositories.role_permission_relation_repository import (
    RolePermissionRelationRepository,
)
from .repositories.student_repository import StudentRepository
from .repositories.teacher_repository import TeacherRepository
from .repositories.classroom_repository import ClassroomRepository
from .repositories.subject_repository import SubjectRepository
from .repositories.classroom_subject_repository import (
    ClassroomSubjectRepository,
)
from .repositories.classroom_subject_student_repository import (
    ClassroomSubjectStudentRepository,
)
from .repositories.classes_repository import ClassesRepository
from .repositories.qualification_repository import (
    QualificationRepository,
)
from .repositories.files_repository import FilesRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.user_repository = UserRepository(session)
        self.role_repository = RoleRepository(session)
        self.permission_repository = PermissionRepository(session)
        self.user_role_relation_repository = UserRoleRelationRepository(
            session
        )
        self.role_permission_relation_repository = (
            RolePermissionRelationRepository(session)
        )
        self.student_repository = StudentRepository(session)
        self.teacher_repository = TeacherRepository(session)
        self.classroom_repository = ClassroomRepository(session)
        self.subject_repository = SubjectRepository(session)
        self.classroom_subject_repository = ClassroomSubjectRepository(
            session
        )
        self.classroom_subject_student_repository = (
            ClassroomSubjectStudentRepository(session)
        )
        self.classes_repository = ClassesRepository(session)
        self.qualification_repository = QualificationRepository(session)
        self.files_repository = FilesRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
