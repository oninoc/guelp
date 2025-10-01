from abc import abstractmethod
from typing import Generic, TypeVar
from ...database import AsyncSQLSession
from .base_data_transfer import BaseDataTransfer
from fastapi import Depends
from ...services.auth import AuthService
from ...persistence.unit_of_work import UnitOfWork

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
        self.unit_of_work = UnitOfWork(session)
        
    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        pass
