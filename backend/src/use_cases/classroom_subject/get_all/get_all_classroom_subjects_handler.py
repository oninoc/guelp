from ...shared.base_auth_handler import BaseAuthHandler
from ....persistence.unit_of_work import UnitOfWork
from .get_all_classroom_subjects_request import GetAllClassroomSubjectsRequest
from .get_all_classroom_subjects_response import GetAllClassroomSubjectsResponse, ClassroomSubjectSummary


class GetAllClassroomSubjectsHandler(BaseAuthHandler[GetAllClassroomSubjectsRequest, GetAllClassroomSubjectsResponse]):
    async def execute(self, request: GetAllClassroomSubjectsRequest) -> GetAllClassroomSubjectsResponse:
        unit_of_work = UnitOfWork(self.session)
        classroom_subjects = await unit_of_work.classroom_subject_repository.get_all_with_relations()

        summaries = []
        for cs in classroom_subjects:
            teacher_name = None
            if cs.teacher:
                teacher_name = f"{cs.teacher.names} {cs.teacher.father_last_name or ''}".strip()
            
            substitute_teacher_name = None
            if cs.substitute_teacher:
                substitute_teacher_name = f"{cs.substitute_teacher.names} {cs.substitute_teacher.father_last_name or ''}".strip()
            
            student_count = len([s for s in cs.students if s.is_active]) if cs.students else 0
            
            summaries.append(
                ClassroomSubjectSummary(
                    id=cs.id,
                    classroom_id=str(cs.classroom_id),
                    classroom_description=cs.classroom.description if cs.classroom else "",
                    subject_id=cs.subject_id,
                    subject_name=cs.subject.name if cs.subject else "",
                    teacher_id=str(cs.teacher_id) if cs.teacher_id else None,
                    teacher_name=teacher_name,
                    substitute_teacher_id=str(cs.substitute_teacher_id) if cs.substitute_teacher_id else None,
                    substitute_teacher_name=substitute_teacher_name,
                    is_active=cs.is_active,
                    student_count=student_count,
                )
            )
        return GetAllClassroomSubjectsResponse(classroom_subjects=summaries)

