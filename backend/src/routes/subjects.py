from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.subjects.create.create_subject_handler import CreateSubjectHandler
from src.use_cases.subjects.create.create_subject_request import CreateSubjectRequest


router = APIRouter()


@router.post("/subjects")
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
