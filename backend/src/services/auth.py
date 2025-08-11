from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from ..config import configuration_variables
from fastapi import HTTPException
from .schemas.auth.CreateAccessTokenResponse import CreateAccessTokenResponse
from .schemas.auth.CreateAccessTokenRequest import CreateAccessTokenRequest, CreateAccessTokenData

class AuthService:
    def __init__(self):
        self.secret_key = configuration_variables.secret_key
        self.algorithm = configuration_variables.algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(self, payload: CreateAccessTokenRequest) -> CreateAccessTokenResponse:
        now_utc = datetime.now(timezone.utc)
        access_expire_at = now_utc + payload.expires_delta

        access_claims = CreateAccessTokenData(
            sub=payload.data.sub,
            email=payload.data.email,
            exp=int(access_expire_at.timestamp()),
            iat=int(now_utc.timestamp()),
            type="access",
        )
        access_token = jwt.encode(access_claims.model_dump(), self.secret_key, algorithm=self.algorithm)

        refresh_expire_at = now_utc + timedelta(days=7)
        refresh_claims = CreateAccessTokenData(
            sub=payload.data.sub,
            email=payload.data.email,
            exp=int(refresh_expire_at.timestamp()),
            iat=int(now_utc.timestamp()),
            type="refresh",
        )
        refresh_token = jwt.encode(refresh_claims.model_dump(), self.secret_key, algorithm=self.algorithm)

        return CreateAccessTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=int(access_expire_at.timestamp()),
        )
    
    def refresh_token(self, token: str) -> CreateAccessTokenResponse:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        subject = payload.get("sub")
        email = payload.get("email")
        if subject is None or email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Create a conventional access token request using subject as the primary claim
        request = CreateAccessTokenRequest(data=CreateAccessTokenData(sub=subject, email=email))
        return self.create_access_token(request)