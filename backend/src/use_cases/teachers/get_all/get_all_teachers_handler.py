from ...shared.base_auth_handler import BaseAuthHandler
from .get_all_teachers_request import GetAllTeachersRequest
from .get_all_teachers_response import GetAllTeachersResponse, TeacherSummary
from ....persistence.repositories.teacher_repository import TeacherRepository


class GetAllTeachersHandler(BaseAuthHandler[GetAllTeachersRequest, GetAllTeachersResponse]):
    async def execute(self, request: GetAllTeachersRequest) -> GetAllTeachersResponse:
        repo = TeacherRepository(self.session)
        teachers = await repo.get_all()
        
        teacher_summaries = [
            TeacherSummary(
                id=str(teacher.id),
                code=teacher.code,
                names=teacher.names,
                father_last_name=teacher.father_last_name,
                mother_last_name=teacher.mother_last_name,
                principal_subject=teacher.principal_subject,
                secondary_subject=teacher.secondary_subject,
            )
            for teacher in teachers
        ]
        
        return GetAllTeachersResponse(teachers=teacher_summaries)
