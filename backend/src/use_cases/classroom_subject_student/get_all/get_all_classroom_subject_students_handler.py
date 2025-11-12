from fastapi import HTTPException

from ...shared.base_auth_handler import BaseAuthHandler
from ....persistence.unit_of_work import UnitOfWork
from .get_all_classroom_subject_students_request import GetAllClassroomSubjectStudentsRequest
from .get_all_classroom_subject_students_response import GetAllClassroomSubjectStudentsResponse, ClassroomSubjectStudentSummary


class GetAllClassroomSubjectStudentsHandler(BaseAuthHandler[GetAllClassroomSubjectStudentsRequest, GetAllClassroomSubjectStudentsResponse]):
    async def execute(self, request: GetAllClassroomSubjectStudentsRequest) -> GetAllClassroomSubjectStudentsResponse:
        unit_of_work = UnitOfWork(self.session)
        
        classroom_subject = await unit_of_work.classroom_subject_repository.get_by_id(request.classroom_subject_id)
        if not classroom_subject:
            raise HTTPException(status_code=404, detail="Classroom-subject not found")
        
        enrollments = await unit_of_work.classroom_subject_student_repository.get_for_classroom_subject(
            request.classroom_subject_id,
            with_relations=True,
            only_active=False,  # Show all students, active and inactive
        )

        summaries = []
        for enrollment in enrollments:
            student = enrollment.student
            if not student:
                continue
            
            summaries.append(
                ClassroomSubjectStudentSummary(
                    id=enrollment.id,
                    student_id=str(student.id),
                    student_code=student.code,
                    student_name=f"{student.names} {student.father_last_name or ''} {student.mother_last_name or ''}".strip(),
                    student_email=student.email,
                    status=enrollment.status,
                    is_active=enrollment.is_active,
                    qualification=enrollment.qualification,
                )
            )
        return GetAllClassroomSubjectStudentsResponse(students=summaries)

