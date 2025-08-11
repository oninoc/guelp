from pydantic import BaseModel
from datetime import timedelta
from typing import Optional

class CreateAccessTokenData(BaseModel):
    sub: str
    email: str
    exp: Optional[int] = None
    iat: Optional[int] = None
    type: Optional[str] = None

class CreateAccessTokenRequest(BaseModel):
    data: CreateAccessTokenData
    expires_delta: Optional[timedelta] = timedelta(minutes=15)