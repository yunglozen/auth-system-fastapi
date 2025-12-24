from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Permissions(BaseModel):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(15), nullable=False)

    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id", ondelete="CASCADE"), nullable=False)
