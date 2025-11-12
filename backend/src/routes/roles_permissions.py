from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.roles_permissions.assign_permission_handler import AssignPermissionHandler
from src.use_cases.roles_permissions.assign_permission_request import AssignPermissionRequest


router = APIRouter()


@router.post("")
async def assign_permission(
    request: AssignPermissionRequest,
    handler: AssignPermissionHandler = Depends(AssignPermissionHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Authorization: requires manage_permissions permission
    if "manage_permissions" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


