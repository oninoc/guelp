from ...shared.base_handler import BaseHandler
from ....persistence.unit_of_work import UnitOfWork
from .get_all_students_request import GetAllStudentsRequest
from .get_all_students_response import GetAllStudentsResponse, StudentSummary


class GetAllStudentsHandler(BaseHandler[GetAllStudentsRequest, GetAllStudentsResponse]):
    async def execute(self, request: GetAllStudentsRequest) -> GetAllStudentsResponse:
        unit_of_work = UnitOfWork(self.session)
        students = await unit_of_work.student_repository.get_all()

        summaries = [
            StudentSummary(
                id=str(student.id),
                code=student.code,
                names=student.names,
                father_last_name=student.father_last_name,
                mother_last_name=student.mother_last_name,
                email=student.email,
            )
            for student in students
        ]

        return GetAllStudentsResponse(students=summaries)


