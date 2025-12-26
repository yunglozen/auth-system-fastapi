from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from datetime import datetime

from .base import BaseModel


class RevokedToken(BaseModel):
    __tablename__ = "revoked_tokens"

    id:  Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
