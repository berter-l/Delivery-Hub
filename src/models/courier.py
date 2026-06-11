from datetime import date, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.types import pk_id
from src.models.base import Base


class Couriers(Base):
    __tablename__ = "couriers"

    id: Mapped[pk_id]
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(25))
    password_hash: Mapped[str] = mapped_column(String(255))
    rating: Mapped[float]
    is_active: Mapped[bool]
    fcm_token: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    balance: Mapped[float]
    total_deliveries: Mapped[int]
