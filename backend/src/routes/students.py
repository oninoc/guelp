from fastapi import APIRouter, Depends, HTTPException
from src.auth import get_current_user, CurrentUserContext
from src.use_cases.students.create.create_student_handler import CreateStudentHandler
from src.use_cases.students.create.create_student_request import CreateStudentRequest
from src.use_cases.students.get_all.get_all_students_handler import (
    GetAllStudentsHandler,
)
from src.use_cases.students.get_all.get_all_students_request import (
    GetAllStudentsRequest,
)
from src.use_cases.students.get_by_id.get_student_by_id_handler import (
    GetStudentByIdHandler,
)
from src.use_cases.students.get_by_id.get_student_by_id_request import (
    GetStudentByIdRequest,
)
from src.use_cases.students.get_subjects.get_student_subjects_handler import (
    GetStudentSubjectsHandler,
)
from src.use_cases.students.get_subjects.get_student_subjects_request import (
    GetStudentSubjectsRequest,
)
from src.use_cases.students.get_subject_qualifications.get_student_subject_qualifications_handler import (
    GetStudentSubjectQualificationsHandler,
)
from src.use_cases.students.get_subject_qualifications.get_student_subject_qualifications_request import (
    GetStudentSubjectQualificationsRequest,
)
from src.use_cases.students.update.update_student_handler import UpdateStudentHandler
from src.use_cases.students.update.update_student_request import UpdateStudentRequest
from src.use_cases.students.delete.delete_student_handler import DeleteStudentHandler
from src.use_cases.students.delete.delete_student_request import DeleteStudentRequest
from src.use_cases.students.generate_notes_pdf.generate_notes_pdf_handler import GenerateNotesPdfHandler
from src.use_cases.students.generate_notes_pdf.generate_notes_pdf_request import GenerateNotesPdfRequest


router = APIRouter()


@router.post("")
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


@router.get("")
async def get_all_students(
    handler: GetAllStudentsHandler = Depends(GetAllStudentsHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetAllStudentsRequest()
    result = await handler.execute(request)
    return {
        **result.model_dump(),
        "requested_by": {
            "email": current.email,
            "roles": current.roles,
            "permissions": current.permissions,
        },
    }


@router.get("/{id}")
async def get_student_by_id(
    id: str,
    handler: GetStudentByIdHandler = Depends(GetStudentByIdHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    request = GetStudentByIdRequest(id=id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/{student_id}/subjects")
async def get_student_subjects(
    student_id: str,
    handler: GetStudentSubjectsHandler = Depends(GetStudentSubjectsHandler),
    current: CurrentUserContext = Depends(get_current_user),
    include_inactive: bool = False,
):
    if current.student_id != student_id and "view_students" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")

    request = GetStudentSubjectsRequest(
        student_id=student_id, include_inactive=include_inactive
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


@router.get("/{student_id}/subjects/qualifications")
async def get_student_subject_qualifications(
    student_id: str,
    handler: GetStudentSubjectQualificationsHandler = Depends(
        GetStudentSubjectQualificationsHandler
    ),
    include_inactive: bool = False,
):
    request = GetStudentSubjectQualificationsRequest(
        student_id=student_id, include_inactive=include_inactive
    )
    result = await handler.execute(request)
    return {**result.model_dump()}


@router.put("/{student_id}")
async def update_student(
    student_id: str,
    request: UpdateStudentRequest,
    handler: UpdateStudentHandler = Depends(UpdateStudentHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request.student_id = student_id
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.delete("/{student_id}")
async def delete_student(
    student_id: str,
    handler: DeleteStudentHandler = Depends(DeleteStudentHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    if "manage_users" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request = DeleteStudentRequest(student_id=student_id)
    result = await handler.execute(request)
    return {**result.model_dump(), "requested_by": {"email": current.email, "roles": current.roles, "permissions": current.permissions}}


@router.get("/{student_id}/notes-pdf")
async def generate_notes_pdf(
    student_id: str,
    include_inactive: bool = False,
    handler: GenerateNotesPdfHandler = Depends(GenerateNotesPdfHandler),
    current: CurrentUserContext = Depends(get_current_user),
):
    # Allow student to download their own notes or admin with view_students permission
    if current.student_id != student_id and "view_students" not in current.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    request = GenerateNotesPdfRequest(student_id=student_id, include_inactive=include_inactive)
    return await handler.execute(request)
