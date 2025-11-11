from fastapi import APIRouter, Depends, HTTPException
from src.auth import (
    get_current_user,
    CurrentUserContext,
    get_optional_current_user,
)
from src.use_cases.subjects.create.create_subject_handler import CreateSubjectHandler
from src.use_cases.subjects.create.create_subject_request import CreateSubjectRequest
from src.use_cases.subjects.get_all.get_all_subjects_handler import (
    GetAllSubjectsHandler,
)
from src.use_cases.subjects.get_all.get_all_subjects_request import (
    GetAllSubjectsRequest,
)


router = APIRouter()


@router.post("/")
async def create_subject(
    request: CreateSubjectRequest,
    handler: CreateSubjectHandler = Depends(CreateSubjectHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Authorization: requires manage_users permission
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/")
async def get_all_subjects(
    handler: GetAllSubjectsHandler = Depends(GetAllSubjectsHandler),
    current: CurrentUserContext | None = Depends(get_optional_current_user),
):
    request = GetAllSubjectsRequest()
    result = await handler.execute(request)
    response = result.model_dump()
    if current is not None:
        response["requested_by"] = {
            "email": current.email,
            "roles": current.roles,
            "permissions": current.permissions,
        }
    return response
