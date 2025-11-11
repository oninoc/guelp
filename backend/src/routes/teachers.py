from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.teachers.create.create_teacher_handler import CreateTeacherHandler
from src.use_cases.teachers.create.create_teacher_request import CreateTeacherRequest
from src.use_cases.teachers.get_by_id.get_teacher_by_id_handler import (
    GetTeacherByIdHandler,
)
from src.use_cases.teachers.get_by_id.get_teacher_by_id_request import (
    GetTeacherByIdRequest,
)
from src.use_cases.teachers.get_all.get_all_teachers_handler import (
    GetAllTeachersHandler,
)
from src.use_cases.teachers.get_all.get_all_teachers_request import (
    GetAllTeachersRequest,
)
from src.use_cases.teachers.get_classrooms_overview.get_teacher_classrooms_handler import (
    GetTeacherClassroomsHandler,
)
from src.use_cases.teachers.get_classrooms_overview.get_teacher_classrooms_request import (
    GetTeacherClassroomsRequest,
)
from src.use_cases.teachers.manage_student_qualification.manage_student_qualification_handler import (
    ManageStudentQualificationHandler,
)
from src.use_cases.teachers.manage_student_qualification.manage_student_qualification_request import (
    ManageStudentQualificationRequest,
)
from src.use_cases.teachers.get_classroom_students.get_teacher_classroom_students_handler import (
    GetTeacherClassroomStudentsHandler,
)
from src.use_cases.teachers.get_classroom_students.get_teacher_classroom_students_request import (
    GetTeacherClassroomStudentsRequest,
)
from src.use_cases.teachers.delete_qualification.delete_qualification_handler import (
    DeleteQualificationHandler,
)
from src.use_cases.teachers.delete_qualification.delete_qualification_request import (
    DeleteQualificationRequest,
)


router = APIRouter()


@router.post("/")
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


@router.get("/{id}")
async def get_teacher_by_id(
    id: str,
    handler: GetTeacherByIdHandler = Depends(GetTeacherByIdHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetTeacherByIdRequest(id=id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/")
async def get_all_teachers(
    handler: GetAllTeachersHandler = Depends(GetAllTeachersHandler),
):
    request = GetAllTeachersRequest()
    result = await handler.execute(request)
    return {**result.model_dump()}


@router.get("/{teacher_id}/classrooms")
async def get_teacher_classrooms(
    teacher_id: str,
    handler: GetTeacherClassroomsHandler = Depends(GetTeacherClassroomsHandler),
    include_inactive: bool = False,
):
    request = GetTeacherClassroomsRequest(
        teacher_id=teacher_id, include_inactive=include_inactive
    )
    result = await handler.execute(request)
    return {**result.model_dump()}


@router.get("/{teacher_id}/classrooms/{classroom_id}/students")
async def get_teacher_classroom_students(
    teacher_id: str,
    classroom_id: str,
    handler: GetTeacherClassroomStudentsHandler = Depends(
        GetTeacherClassroomStudentsHandler
    ),
    include_inactive: bool = False,
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetTeacherClassroomStudentsRequest(
        teacher_id=teacher_id,
        classroom_id=classroom_id,
        requesting_user_id=current.user_id,
        can_manage_any="manage_users" in current.permissions,
        include_inactive=include_inactive,
    )
    result = await handler.execute(request)
    return {
        **result.model_dump(),
        "requested_by": {
            "email": current.email,
            "roles": current.roles,
            "permissions": current.permissions,
        },
    }


@router.post("/{teacher_id}/qualifications")
async def manage_student_qualification(
    teacher_id: str,
    payload: ManageStudentQualificationRequest,
    handler: ManageStudentQualificationHandler = Depends(
        ManageStudentQualificationHandler
    ),
    current: CurrentUserContext = Depends(get_current_user),
):
    try:
        teacher_uuid = UUID(teacher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid teacher identifier")

    teacher = await handler.unit_of_work.teacher_repository.get_by_id(teacher_uuid)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    if str(teacher.user_id) != current.user_id and "manage_qualifications" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    request = payload.model_copy(update={"teacher_id": teacher_uuid})
    result = await handler.execute(request)
    return {
        **result.model_dump(),
        "requested_by": {
            "email": current.email,
            "roles": current.roles,
            "permissions": current.permissions,
        },
    }


@router.delete("/{teacher_id}/qualifications/{qualification_id}")
async def delete_qualification(
    teacher_id: str,
    qualification_id: int,
    handler: DeleteQualificationHandler = Depends(DeleteQualificationHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    try:
        teacher_uuid = UUID(teacher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid teacher identifier")

    teacher = await handler.unit_of_work.teacher_repository.get_by_id(teacher_uuid)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    if str(teacher.user_id) != current.user_id and "manage_qualifications" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    request = DeleteQualificationRequest(
        teacher_id=teacher_uuid,
        qualification_id=qualification_id,
    )
    result = await handler.execute(request)
    return {
        **result.model_dump(),
        "requested_by": {
            "email": current.email,
            "roles": current.roles,
            "permissions": current.permissions,
        },
    }
