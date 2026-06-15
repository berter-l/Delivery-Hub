from datetime import date, datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.types import pk_id
from src.models.base import Base


class Couriers(Base):
    __tablename__ = "couriers"

    id: Mapped[pk_id]
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(25))
    password_hash: Mapped[str] = mapped_column(String(255))
    rating: Mapped[float]
    is_active: Mapped[bool]
    fcm_token: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    balance: Mapped[float]
    total_deliveries: Mapped[int]
    orders: Mapped[list["Orders"]] = relationship(back_populates="courier")
