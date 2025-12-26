from pydantic import BaseModel, EmailStr, Field

from datetime import datetime

__all__ = ["UserCreate", "UserRead", "UserLogin", "UserUpdate"]


class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    password_repeat: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
