from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.students.create.create_student_handler import CreateStudentHandler
from src.use_cases.students.create.create_student_request import CreateStudentRequest
from src.use_cases.students.get_by_id.get_student_by_id_handler import GetStudentByIdHandler
from src.use_cases.students.get_by_id.get_student_by_id_request import GetStudentByIdRequest


router = APIRouter()


@router.post("/students")
async def create_student(
    request: CreateStudentRequest,
    handler: CreateStudentHandler = Depends(CreateStudentHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Authorization: requires manage_users permission
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/student/{id}")
async def get_student_by_id(
    id: str,
    handler: GetStudentByIdHandler = Depends(GetStudentByIdHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetStudentByIdRequest(id=id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}
