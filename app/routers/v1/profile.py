from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.core.database import get_async_session
from app.core.dependencies import get_current_user, require_permission

from app.models.user import User

from app.schemas.user import UserUpdate


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/info", dependencies=[Depends(require_permission("profile", "read"))])
async def profile(
        current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "middle_name": current_user.middle_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }


@router.put("/update", dependencies=[Depends(require_permission("profile", "write"))])
async def update_profile(
        data: UserUpdate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    update_data = data.dict(exclude_unset=True)

    stmt = (update(User).where(User.id == current_user.id).values(**update_data)
            .execution_options(synchronize_session="fetch"))

    await session.execute(stmt)

    return {"Message": "Profile updated successfully"}