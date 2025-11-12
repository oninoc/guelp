from fastapi import HTTPException
from uuid import uuid4

from ...shared.base_auth_handler import BaseAuthHandler
from .create_student_request import CreateStudentRequest
from .create_student_response import CreateStudentResponse
from ....models.students import Student
from ....models.user import User


class CreateStudentHandler(BaseAuthHandler[CreateStudentRequest, CreateStudentResponse]):
    async def execute(self, request: CreateStudentRequest) -> CreateStudentResponse:
        # Auto-create user if user_id not provided but user_email and user_password are
        user_id = request.user_id
        if not user_id and request.user_email and request.user_password:
            # Check if email already exists
            existing = await self.unit_of_work.user_repository.get_by_email(request.user_email)
            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            # Create user
            hashed = self.auth_service.get_password_hash(request.user_password)
            user = User(
                name=request.names,
                last_name=request.father_last_name or "",
                phone=request.phone or "",
                address=request.address or "",
                email=request.user_email,
                password=hashed,
                token=uuid4().hex,
                refresh_token=uuid4().hex,
            )
            created_user = await self.unit_of_work.user_repository.create(user)
            user_id = str(created_user.id)
        elif not user_id:
            raise HTTPException(
                status_code=400,
                detail="Either user_id or both user_email and user_password must be provided"
            )

        student = Student(
            code=request.code,
            names=request.names,
            father_last_name=request.father_last_name,
            mother_last_name=request.mother_last_name,
            phone=request.phone,
            address=request.address,
            email=request.email,
            birth_date=request.birth_date,
            gender=request.gender,
            document_type=request.document_type,
            document_number=request.document_number,
            responsible_name=request.responsible_name,
            responsible_phone=request.responsible_phone,
            responsible_email=request.responsible_email,
            responsible_address=request.responsible_address,
            user_id=user_id,
        )

        created = await self.unit_of_work.student_repository.create(student)
        return CreateStudentResponse(
            id=str(created.id),
            code=created.code,
            names=created.names,
            father_last_name=created.father_last_name,
            mother_last_name=created.mother_last_name,
            full_name=created.full_name,
            email=created.email,
            phone=created.phone,
        )
