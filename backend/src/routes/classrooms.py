from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.classrooms.create.create_classroom_handler import CreateClassroomHandler
from src.use_cases.classrooms.create.create_classroom_request import CreateClassroomRequest
from src.use_cases.classrooms.get_all.get_all_classrooms_handler import GetAllClassroomsHandler
from src.use_cases.classrooms.get_all.get_all_classrooms_request import GetAllClassroomsRequest
from src.use_cases.classrooms.get_by_id.get_classroom_by_id_handler import GetClassroomByIdHandler
from src.use_cases.classrooms.get_by_id.get_classroom_by_id_request import GetClassroomByIdRequest
from src.use_cases.classrooms.update.update_classroom_handler import UpdateClassroomHandler
from src.use_cases.classrooms.update.update_classroom_request import UpdateClassroomRequest
from src.use_cases.classrooms.delete.delete_classroom_handler import DeleteClassroomHandler
from src.use_cases.classrooms.delete.delete_classroom_request import DeleteClassroomRequest


router = APIRouter()


@router.post("")
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


@router.get("")
async def get_all_classrooms(
    handler: GetAllClassroomsHandler = Depends(GetAllClassroomsHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request = GetAllClassroomsRequest()
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/{classroom_id}")
async def get_classroom_by_id(
    classroom_id: str,
    handler: GetClassroomByIdHandler = Depends(GetClassroomByIdHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetClassroomByIdRequest(id=classroom_id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.put("/{classroom_id}")
async def update_classroom(
    classroom_id: str,
    request: UpdateClassroomRequest,
    handler: UpdateClassroomHandler = Depends(UpdateClassroomHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request.classroom_id = classroom_id
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.delete("/{classroom_id}")
async def delete_classroom(
    classroom_id: str,
    handler: DeleteClassroomHandler = Depends(DeleteClassroomHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request = DeleteClassroomRequest(classroom_id=classroom_id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}
