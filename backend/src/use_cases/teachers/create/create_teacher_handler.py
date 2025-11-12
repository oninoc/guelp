from fastapi import HTTPException
from uuid import uuid4

from ...shared.base_auth_handler import BaseAuthHandler
from .create_teacher_request import CreateTeacherRequest
from .create_teacher_response import CreateTeacherResponse
from ....models.teachers import Teacher
from ....models.user import User


class CreateTeacherHandler(BaseAuthHandler[CreateTeacherRequest, CreateTeacherResponse]):
    async def execute(self, request: CreateTeacherRequest) -> CreateTeacherResponse:
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
                phone="",
                address="",
                email=request.user_email,
                password=hashed,
                token=uuid4().hex,
                refresh_token=uuid4().hex,
            )
            created_user = await self.unit_of_work.user_repository.create(user)
            user_id = created_user.id
        elif not user_id:
            raise HTTPException(
                status_code=400,
                detail="Either user_id or both user_email and user_password must be provided"
            )

        teacher = Teacher(
            names=request.names,
            father_last_name=request.father_last_name,
            mother_last_name=request.mother_last_name,
            document_type=request.document_type,
            document_number=request.document_number,
            birth_date=request.birth_date,
            gender=request.gender,
            user_id=user_id,
        )
        
        created = await self.unit_of_work.teacher_repository.create(teacher)
        return CreateTeacherResponse(
            id=str(created.id),
            names=created.names,
            father_last_name=created.father_last_name,
            mother_last_name=created.mother_last_name,
            document_type=created.document_type,
            document_number=created.document_number,
            birth_date=created.birth_date,
            gender=created.gender,
            user_id=str(created.user_id),
        )
