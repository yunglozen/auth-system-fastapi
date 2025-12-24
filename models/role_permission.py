from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class RolePermission(BaseModel):
    role_id: Mapped = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
