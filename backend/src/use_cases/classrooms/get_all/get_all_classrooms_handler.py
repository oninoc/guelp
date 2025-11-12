from ...shared.base_handler import BaseHandler
from ....persistence.unit_of_work import UnitOfWork
from .get_all_classrooms_request import GetAllClassroomsRequest
from .get_all_classrooms_response import GetAllClassroomsResponse, ClassroomSummary


class GetAllClassroomsHandler(BaseHandler[GetAllClassroomsRequest, GetAllClassroomsResponse]):
    async def execute(self, request: GetAllClassroomsRequest) -> GetAllClassroomsResponse:
        unit_of_work = UnitOfWork(self.session)
        classrooms = await unit_of_work.classroom_repository.get_all_with_relations()

        summaries = []
        for classroom in classrooms:
            tutor_name = None
            if classroom.tutor:
                tutor_name = f"{classroom.tutor.names} {classroom.tutor.father_last_name or ''}".strip()
            
            summaries.append(
                ClassroomSummary(
                    id=str(classroom.id),
                    description=classroom.description,
                    level=classroom.level,
                    degree=classroom.degree,
                    tutor_id=str(classroom.tutor_id) if classroom.tutor_id else None,
                    tutor_name=tutor_name,
                )
            )
        return GetAllClassroomsResponse(classrooms=summaries)

