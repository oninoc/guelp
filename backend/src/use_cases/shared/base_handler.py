from abc import abstractmethod
from typing import Generic, TypeVar

from ...persistence.unit_of_work import UnitOfWork
from ...database import AsyncSQLSession
from .base_data_transfer import BaseDataTransfer
from fastapi import Depends

TRequest = TypeVar("TRequest", bound=BaseDataTransfer)
TResponse = TypeVar("TResponse", bound=BaseDataTransfer)


class BaseHandler(Generic[TRequest, TResponse]):

    def __init__(
        self,
        session: AsyncSQLSession,
    ):
        self.session = session
        self.unit_of_work = UnitOfWork(session)
        
    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        pass
