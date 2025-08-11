from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .config import configuration_variables
from typing import Annotated, AsyncGenerator

data_base_url = configuration_variables.database_url.replace(
    "postgresql:", "postgresql+psycopg:"
)

engine = create_async_engine(
    data_base_url, echo=configuration_variables.log_sql_queries
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


AsyncSQLSession = Annotated[AsyncSession, Depends(get_session)]
