from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from core.security import decode_access_token
from core.database import get_async_session

from models.user import User
from models.role import Role
from models.resource import Resource
from models.permission import Permission
from models.revoked_token import RevokedToken

__all__ = ["get_current_user", "require_permission"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    stmt = select(RevokedToken).where(RevokedToken.token == token)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=401, detail="Token revoked")

    stmt = select(User).where(User.id == int(user_id))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive or deleted")

    return user


def require_permission(resource_name: str, action: str):
    async def checker(
            current_user: User = Depends(get_current_user),
            session: AsyncSession = Depends(get_async_session)
    ):
        stmt = (
            select(Permission)
            .join(Permission.roles)
            .join(Role.users)
            .join(Permission.resources)
            .where(
                User.id == current_user.id,
                Resource.name == resource_name,
                Permission.action == action
            )
        )

        result = await session.execute(stmt)
        permission = result.scalar_one_or_none()

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )

        return True

    return checker
