from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.classrooms.create.create_classroom_handler import CreateClassroomHandler
from src.use_cases.classrooms.create.create_classroom_request import CreateClassroomRequest


router = APIRouter()


@router.post("/classrooms")
async def create_classroom(
    request: CreateClassroomRequest,
    handler: CreateClassroomHandler = Depends(CreateClassroomHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Authorization: requires manage_users permission
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}
