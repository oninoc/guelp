from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .create_classroom_subject_student_request import CreateClassroomSubjectStudentRequest
from .create_classroom_subject_student_response import CreateClassroomSubjectStudentResponse
from ....models.classroom_subject_student import ClassroomSubjectStudent


class CreateClassroomSubjectStudentHandler(BaseAuthHandler[CreateClassroomSubjectStudentRequest, CreateClassroomSubjectStudentResponse]):
    async def execute(self, request: CreateClassroomSubjectStudentRequest) -> CreateClassroomSubjectStudentResponse:
        student_id = UUID(request.student_id)
        student = await self.unit_of_work.student_repository.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        classroom_subject = await self.unit_of_work.classroom_subject_repository.get_by_id(request.classroom_subject_id)
        if not classroom_subject:
            raise HTTPException(status_code=404, detail="Classroom-subject relation not found")

        # Check if already enrolled
        existing = await self.unit_of_work.classroom_subject_student_repository.get_by_unique_relation(
            request.classroom_subject_id, student_id
        )
        if existing:
            raise HTTPException(status_code=400, detail="Student already enrolled in this classroom-subject")

        enrollment = ClassroomSubjectStudent(
            classroom_subject_id=request.classroom_subject_id,
            student_id=student_id,
            status=request.status,
            is_active=request.is_active,
        )

        created = await self.unit_of_work.classroom_subject_student_repository.create(enrollment)
        
        return CreateClassroomSubjectStudentResponse(
            id=created.id,
            classroom_subject_id=created.classroom_subject_id,
            student_id=str(created.student_id),
            status=created.status,
            is_active=created.is_active,
        )

