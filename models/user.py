from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    first_name: Mapped[str | None] = mapped_column(String(30))
    last_name: Mapped[str | None] = mapped_column(String(30))
    middle_name: Mapped[str | None] = mapped_column(String(30))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped = mapped_column(DateTime(timezone=True), onupdate=func.now())
