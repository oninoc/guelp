from ...shared.base_auth_handler import BaseAuthHandler
from .get_all_teachers_request import GetAllTeachersRequest
from .get_all_teachers_response import GetAllTeachersResponse, TeacherSummary

class GetAllTeachersHandler(BaseAuthHandler[GetAllTeachersRequest, GetAllTeachersResponse]):
    async def execute(self, request: GetAllTeachersRequest) -> GetAllTeachersResponse:
        teachers = await self.unit_of_work.teacher_repository.get_all()
        
        teacher_summaries = [
            TeacherSummary(
                id=str(teacher.id),
                names=teacher.names,
                father_last_name=teacher.father_last_name,
                mother_last_name=teacher.mother_last_name,
                document_type=teacher.document_type,
                document_number=teacher.document_number,
            )
            for teacher in teachers
        ]
        
        return GetAllTeachersResponse(teachers=teacher_summaries)
