from pydantic import BaseModel

class CreateAccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int 