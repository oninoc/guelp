from abc import abstractmethod
from typing import Generic, TypeVar
from ...database import AsyncSQLSession
from .base_data_transfer import BaseDataTransfer
from fastapi import Depends
from ...services.auth import AuthService
from ...persistence.user_unit_work import UserUnitOfWork

TRequest = TypeVar("TRequest", bound=BaseDataTransfer)
TResponse = TypeVar("TResponse", bound=BaseDataTransfer)


class BaseAuthHandler(Generic[TRequest, TResponse]):
    def __init__(
        self,
        session: AsyncSQLSession,
        auth_service: AuthService = Depends(AuthService),
    ):
        self.session = session
        self.auth_service = auth_service
        self.user_unit_of_work = UserUnitOfWork(session)
        
    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        pass
