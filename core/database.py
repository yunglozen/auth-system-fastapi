from typing import AsyncGenerator, Optional, Callable
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from models.base import BaseModel
from models.user import User
from models.role import Role
from models.resource import Resource
from models.permission import Permission
from models.user_roles import UserRole
from models.role_permission import RolePermission
from models.revoked_token import RevokedToken
from .settings import settings

__all__ = ["global_init", "get_async_session", "create_db_and_tables", "delete_db_and_tables"]

__async_engine: Optional[AsyncEngine] = None
__session_factory: Optional[Callable[[], AsyncSession]] = None

SQLALCHEMY_DATABASE_URL = settings.database_url


def global_init() -> None:
    global __async_engine, __session_factory

    if __session_factory:
        return

    if not __async_engine:
        __async_engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL, echo=False)

    __session_factory = async_sessionmaker(__async_engine)


async def get_async_session() -> AsyncGenerator:
    global __session_factory

    if not __session_factory:
        raise ValueError({"message": "You must call global_init() before using this method."})

    session: AsyncSession = __session_factory()

    try:
        yield session
        await session.commit()
    except Exception as e:
        raise e
    finally:
        await session.rollback()
        await session.close()


async def create_db_and_tables():
    global __async_engine

    if __async_engine is None:
        raise ValueError({"message": "You must call global_init() before using this method."})

    async with __async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def delete_db_and_tables():
    global __async_engine

    if __async_engine is None:
        raise ValueError({"message": "You must call global_init() before using this method."})

    async with __async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


