from ...shared.base_auth_handler import BaseAuthHandler
from .login_request import LoginRequest
from .login_response import LoginResponse
from fastapi import HTTPException
from ....services.schemas.auth.CreateAccessTokenRequest import CreateAccessTokenRequest, CreateAccessTokenData

class LoginHandler(BaseAuthHandler[LoginRequest, LoginResponse]):
    async def execute(self, request: LoginRequest) -> LoginResponse:
        user = await self.user_unit_of_work.user_repository.get_by_email(request.email)
        if not self.auth_service.verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token_response = self.auth_service.create_access_token(
            CreateAccessTokenRequest(
                data=CreateAccessTokenData(
                    sub=str(user.id),
                    email=user.email,
                )
            )
        )
        # Persist tokens on login
        user.token = token_response.access_token
        user.refresh_token = token_response.refresh_token
        await self.user_unit_of_work.user_repository.update(user)

        return LoginResponse(
            access_token=token_response.access_token,
            refresh_token=token_response.refresh_token,
            expires_at=token_response.expires_at,
        )