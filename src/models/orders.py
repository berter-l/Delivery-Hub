from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.models.base import Base


class Orders(Base):
    __tablename__ = 'orders'

    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id', ondelete='CASCADE'))
    courier_id: Mapped[int | None] = mapped_column(ForeignKey('couriers.id'))
    courier: Mapped["Couriers"] = relationship(back_populates="orders")
    pickup_address: Mapped[str]
    delivery_address: Mapped[str]
    delivery_fee: Mapped[float]
    accepted_at: Mapped[datetime | None]
    delivered_at: Mapped[datetime | None]
