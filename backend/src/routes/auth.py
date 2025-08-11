from fastapi import APIRouter, Depends
from src.use_cases.user.login.login_handler import LoginHandler
from src.use_cases.user.login.login_request import LoginRequest

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest, handler: LoginHandler = Depends(LoginHandler)):
    return await handler.execute(request)  