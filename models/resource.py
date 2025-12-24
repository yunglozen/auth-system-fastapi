from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Resources(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)

    permissions = relationship("Permission", back_populates="resource", cascade="all, delete-orphan")
