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
from src.use_cases.subjects.get_by_id.get_subject_by_id_handler import GetSubjectByIdHandler
from src.use_cases.subjects.get_by_id.get_subject_by_id_request import GetSubjectByIdRequest
from src.use_cases.subjects.update.update_subject_handler import UpdateSubjectHandler
from src.use_cases.subjects.update.update_subject_request import UpdateSubjectRequest
from src.use_cases.subjects.delete.delete_subject_handler import DeleteSubjectHandler
from src.use_cases.subjects.delete.delete_subject_request import DeleteSubjectRequest


router = APIRouter()


@router.post("")
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


@router.get("")
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


@router.get("/{subject_id}")
async def get_subject_by_id(
    subject_id: int,
    handler: GetSubjectByIdHandler = Depends(GetSubjectByIdHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetSubjectByIdRequest(id=subject_id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.put("/{subject_id}")
async def update_subject(
    subject_id: int,
    request: UpdateSubjectRequest,
    handler: UpdateSubjectHandler = Depends(UpdateSubjectHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Set subject_id from path parameter
    request.subject_id = subject_id
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.delete("/{subject_id}")
async def delete_subject(
    subject_id: int,
    handler: DeleteSubjectHandler = Depends(DeleteSubjectHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request = DeleteSubjectRequest(subject_id=subject_id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}
