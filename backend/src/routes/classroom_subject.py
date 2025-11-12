from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.classroom_subject.create.create_classroom_subject_handler import CreateClassroomSubjectHandler
from src.use_cases.classroom_subject.create.create_classroom_subject_request import CreateClassroomSubjectRequest
from src.use_cases.classroom_subject.get_all.get_all_classroom_subjects_handler import GetAllClassroomSubjectsHandler
from src.use_cases.classroom_subject.get_all.get_all_classroom_subjects_request import GetAllClassroomSubjectsRequest


router = APIRouter()


@router.post("")
async def create_classroom_subject(
    request: CreateClassroomSubjectRequest,
    handler: CreateClassroomSubjectHandler = Depends(CreateClassroomSubjectHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("")
async def get_all_classroom_subjects(
    handler: GetAllClassroomSubjectsHandler = Depends(GetAllClassroomSubjectsHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request = GetAllClassroomSubjectsRequest()
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}

