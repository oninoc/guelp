from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.user.create.create_user_handler import CreateUserHandler
from src.use_cases.user.create.create_user_request import CreateUserRequest
from src.use_cases.user.get_by_id.get_user_by_id_handler import GetUserByIdHandler
from src.use_cases.user.get_by_id.get_user_by_id_request import GetUserByIdRequest


router = APIRouter()


@router.post("/users")
async def create_user(
    request: CreateUserRequest,
    handler: CreateUserHandler = Depends(CreateUserHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Authorization: requires manage_users permission
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    created = await handler.execute(request)
    return {**created.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}

@router.get("/user/{id}")
async def get_user_by_id(
    id: str,
    handler: GetUserByIdHandler = Depends(GetUserByIdHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if ("manage_users" not in current.permissions) and (current.user_id != id):
        raise HTTPException(status_code=403, detail="Forbidden")

    request = GetUserByIdRequest(id=id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


