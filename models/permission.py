from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Permissions(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(15), nullable=False)

    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id", ondelete="CASCADE"), nullable=False)

    resource = relationship("Resource", back_populates="permissions")
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
