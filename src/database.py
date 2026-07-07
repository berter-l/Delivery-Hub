from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings
from typing import Annotated

from sqlalchemy.orm import mapped_column

pk_id = Annotated[int, mapped_column(primary_key=True)]
str_100 = Annotated[str, String(100)]
engine = create_async_engine(settings.db.get_db_url, echo=settings.db.ECHO)

session = async_sessionmaker(engine)


async def get_session():
    async with session() as session_db:
        yield session_db
