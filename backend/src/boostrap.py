from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import Dict

from src.config import configuration_variables
from src.routes.auth import router as auth_router
from src.routes.users import router as users_router
from src.routes.roles import router as roles_router
from src.routes.roles_permissions import router as roles_permissions_router
from src.routes.teachers import router as teachers_router
from src.routes.students import router as students_router
from src.routes.classrooms import router as classrooms_router
from src.routes.subjects import router as subjects_router

app: FastAPI = FastAPI()

if configuration_variables.is_production:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

frontend_origins = {
    "http://localhost:8081",  # Expo web default
    "http://localhost:19006",  # Expo web alternative
    "http://localhost:19000",  # Expo dev server
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")
app.include_router(roles_router, prefix="/roles")
app.include_router(roles_permissions_router, prefix="/permissions")
app.include_router(teachers_router, prefix="/teachers")
app.include_router(students_router, prefix="/students")
app.include_router(classrooms_router, prefix="/classrooms")
app.include_router(subjects_router, prefix="/subjects")