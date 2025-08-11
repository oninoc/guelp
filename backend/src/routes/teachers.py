from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.teachers.create.create_teacher_handler import CreateTeacherHandler
from src.use_cases.teachers.create.create_teacher_request import CreateTeacherRequest
from src.use_cases.teachers.get_by_id.get_teacher_by_id_handler import GetTeacherByIdHandler
from src.use_cases.teachers.get_by_id.get_teacher_by_id_request import GetTeacherByIdRequest
from src.use_cases.teachers.get_all.get_all_teachers_handler import GetAllTeachersHandler
from src.use_cases.teachers.get_all.get_all_teachers_request import GetAllTeachersRequest


router = APIRouter()


@router.post("/teachers")
async def create_teacher(
    request: CreateTeacherRequest,
    handler: CreateTeacherHandler = Depends(CreateTeacherHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Authorization: requires manage_users permission
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/teacher/{id}")
async def get_teacher_by_id(
    id: str,
    handler: GetTeacherByIdHandler = Depends(GetTeacherByIdHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetTeacherByIdRequest(id=id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/teachers")
async def get_all_teachers(
    handler: GetAllTeachersHandler = Depends(GetAllTeachersHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetAllTeachersRequest()
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}
