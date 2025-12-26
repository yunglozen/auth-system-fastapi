from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import require_permission, get_current_user
from core.database import get_async_session

from models.user import User
from models.role import Role
from models.resource import Resource
from models.permission import Permission
from models.user_roles import UserRole
from models.role_permission import RolePermission

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/roles", dependencies=[Depends(require_permission("panel", "write"))])
async def create_role(
        name: str,
        description: str | None = None,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    role = Role(name=name, description=description)
    session.add(role)

    return role


@router.post("/resources", dependencies=[Depends(require_permission("panel", "write"))])
async def create_resource(
        name: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    resource = Resource(name=name)
    session.add(resource)

    return resource


@router.post("/permissions", dependencies=[Depends(require_permission("panel", "write"))])
async def create_permission(
        action: str,
        resource_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    permission = Permission(action=action, resource_id=resource_id)
    session.add(permission)

    return permission


@router.post("/user_roles", dependencies=[Depends(require_permission("panel", "write"))])
async def assign_role(
        user_id: int,
        role_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_role = UserRole(user_id=user_id, role_id=role_id)
    session.add(user_role)

    return {"msg": "Role assigned"}


@router.post("/role_permissions", dependencies=[Depends(require_permission("panel", "write"))])
async def assign_permission(
        role_id: int,
        permission_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    role_perm = RolePermission(role_id=role_id, permission_id=permission_id)
    session.add(role_perm)

    return {"msg": "Permission assigned"}