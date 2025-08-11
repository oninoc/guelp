from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.roles.assign_role_handler import AssignRoleHandler
from src.use_cases.roles.assign_role_request import AssignRoleRequest


router = APIRouter()


@router.post("/roles")
async def assign_role(
    request: AssignRoleRequest,
    handler: AssignRoleHandler = Depends(AssignRoleHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Authorization: requires manage_roles permission
    if "manage_roles" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


