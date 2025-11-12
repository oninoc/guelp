from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .create_classroom_subject_request import CreateClassroomSubjectRequest
from .create_classroom_subject_response import CreateClassroomSubjectResponse
from ....models.classroom_subject import ClassroomSubject


class CreateClassroomSubjectHandler(BaseAuthHandler[CreateClassroomSubjectRequest, CreateClassroomSubjectResponse]):
    async def execute(self, request: CreateClassroomSubjectRequest) -> CreateClassroomSubjectResponse:
        classroom_id = UUID(request.classroom_id)
        classroom = await self.unit_of_work.classroom_repository.get_by_id(classroom_id)
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")

        subject = await self.unit_of_work.subject_repository.get_by_id(request.subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        teacher_id = None
        if request.teacher_id:
            teacher_id = UUID(request.teacher_id)
            teacher = await self.unit_of_work.teacher_repository.get_by_id(teacher_id)
            if not teacher:
                raise HTTPException(status_code=404, detail="Teacher not found")

        substitute_teacher_id = None
        if request.substitute_teacher_id:
            substitute_teacher_id = UUID(request.substitute_teacher_id)
            substitute_teacher = await self.unit_of_work.teacher_repository.get_by_id(substitute_teacher_id)
            if not substitute_teacher:
                raise HTTPException(status_code=404, detail="Substitute teacher not found")

        # Check if already exists
        existing = await self.unit_of_work.classroom_subject_repository.get_by_classroom_and_subject(
            classroom_id, request.subject_id
        )
        if existing:
            raise HTTPException(status_code=400, detail="Classroom-subject relation already exists")

        classroom_subject = ClassroomSubject(
            classroom_id=classroom_id,
            subject_id=request.subject_id,
            teacher_id=teacher_id,
            substitute_teacher_id=substitute_teacher_id,
            is_active=request.is_active,
        )

        created = await self.unit_of_work.classroom_subject_repository.create(classroom_subject)
        
        return CreateClassroomSubjectResponse(
            id=created.id,
            classroom_id=str(created.classroom_id),
            subject_id=created.subject_id,
            teacher_id=str(created.teacher_id) if created.teacher_id else None,
            substitute_teacher_id=str(created.substitute_teacher_id) if created.substitute_teacher_id else None,
            is_active=created.is_active,
        )

