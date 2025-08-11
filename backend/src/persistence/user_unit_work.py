from sqlalchemy.ext.asyncio import AsyncSession
from .repositories.user_repository import UserRepository


class UserUnitOfWork:
    _session: AsyncSession
    user_repository: UserRepository

    def __init__(self, session: AsyncSession):
        self._session = session
        self.user_repository = UserRepository(session)
