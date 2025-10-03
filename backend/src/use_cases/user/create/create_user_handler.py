from ...shared.base_auth_handler import BaseAuthHandler
from .create_user_request import CreateUserRequest
from .create_user_response import CreateUserResponse
from fastapi import HTTPException
from ....models.user import User
from uuid import uuid4


class CreateUserHandler(BaseAuthHandler[CreateUserRequest, CreateUserResponse]):
    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # Authorization must be enforced in route dependency; double-check here for safety if desired
        existing = await self.unit_of_work.user_repository.get_by_email(request.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed = self.auth_service.get_password_hash(request.password)
        user = User(
            name=request.name,
            last_name=request.last_name,
            phone=request.phone,
            address=request.address,
            email=request.email,
            password=hashed,
            token=uuid4().hex,
            refresh_token=uuid4().hex,
        )
        created = await self.unit_of_work.user_repository.create(user)
        return CreateUserResponse(id=str(created.id), email=created.email)


