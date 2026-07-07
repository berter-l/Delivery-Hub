from datetime import date, datetime

from sqlalchemy import String, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import str_100
from src.models.base import Base, Roles


class Couriers(Base):
    __tablename__ = "couriers"

    first_name: Mapped[str_100]
    last_name: Mapped[str_100]
    phone: Mapped[str] = mapped_column(String(25))
    password_hash: Mapped[bytes]
    rating: Mapped[float] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=False)
    fcm_token: Mapped[str] = mapped_column(String(255), unique=True)
    balance: Mapped[float] = mapped_column(default=0)
    total_deliveries: Mapped[int] = mapped_column(default=0)
    orders: Mapped[list["Orders"]] = relationship(back_populates="courier")
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Roles] = mapped_column(Enum(Roles, validate_strings=True, create_constraint=True))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
