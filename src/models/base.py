from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.database import pk_id

default_type = Annotated[bool, mapped_column(default=False)]


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[pk_id]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class PermissionsMixin():
    is_admin: Mapped[default_type]
    is_courier: Mapped[default_type]
    is_partner: Mapped[default_type]
