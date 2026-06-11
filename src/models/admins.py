from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.types import pk_id
from src.models.base import Base


class Admins(Base):
    __tablename__ = 'admins'

    id: Mapped[pk_id]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
