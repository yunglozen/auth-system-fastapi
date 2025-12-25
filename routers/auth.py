from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from datetime import datetime

from core.database import get_async_session
from core.security import hash_password, verify_password, create_access_token
from models.user import User
from models.revoked_token import RevokedToken
from schemas.user import UserCreate, UserLogin
from core.dependencies import get_current_user, oauth2_scheme


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        data: UserCreate,
        session: AsyncSession = Depends(get_async_session)
):
    if data.password != data.password_repeat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    stmt = select(User).where(User.email == data.email)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        is_active=True
    )

    session.add(user)

    return {"Message": "User registered successfully"}


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(User).where(User.email == form_data.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(user_id=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/delete-account")
async def delete_account(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    current_user.is_active = False

    return {"Message": "User account has been deactivated and logged out."}


@router.post("/logout")
async def logout(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(RevokedToken).where(RevokedToken.token == token)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Token already revoked")

    stmt = insert(RevokedToken).values(token=token, revoked_at=datetime.utcnow())
    await session.execute(stmt)

    return {"Message": "Successfully logged out"}
