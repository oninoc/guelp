from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.classroom_subject_student.create.create_classroom_subject_student_handler import CreateClassroomSubjectStudentHandler
from src.use_cases.classroom_subject_student.create.create_classroom_subject_student_request import CreateClassroomSubjectStudentRequest
from src.use_cases.classroom_subject_student.get_all.get_all_classroom_subject_students_handler import GetAllClassroomSubjectStudentsHandler
from src.use_cases.classroom_subject_student.get_all.get_all_classroom_subject_students_request import GetAllClassroomSubjectStudentsRequest


router = APIRouter()


@router.post("")
async def create_classroom_subject_student(
    request: CreateClassroomSubjectStudentRequest,
    handler: CreateClassroomSubjectStudentHandler = Depends(CreateClassroomSubjectStudentHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/classroom-subject/{classroom_subject_id}")
async def get_classroom_subject_students(
    classroom_subject_id: int,
    handler: GetAllClassroomSubjectStudentsHandler = Depends(GetAllClassroomSubjectStudentsHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request = GetAllClassroomSubjectStudentsRequest(classroom_subject_id=classroom_subject_id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}

