from ...shared.base_auth_handler import BaseAuthHandler
from .get_teacher_by_id_request import GetTeacherByIdRequest
from .get_teacher_by_id_response import GetTeacherByIdResponse
from ....persistence.repositories.teacher_repository import TeacherRepository
from fastapi import HTTPException


class GetTeacherByIdHandler(BaseAuthHandler[GetTeacherByIdRequest, GetTeacherByIdResponse]):
    async def execute(self, request: GetTeacherByIdRequest) -> GetTeacherByIdResponse:
        repo = TeacherRepository(self.session)
        teacher = await repo.get_by_id(str(request.id))
        
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        return GetTeacherByIdResponse(
            id=str(teacher.id),
            code=teacher.code,
            names=teacher.names,
            father_last_name=teacher.father_last_name,
            mother_last_name=teacher.mother_last_name,
            document_type=teacher.document_type,
            document_number=teacher.document_number,
            birth_date=teacher.birth_date,
            gender=teacher.gender,
            nationality=teacher.nationality,
            principal_subject=teacher.principal_subject,
            secondary_subject=teacher.secondary_subject,
            start_time=teacher.start_time,
            end_time=teacher.end_time,
            user_id=teacher.user_id,
        )
