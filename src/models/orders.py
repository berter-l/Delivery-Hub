from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.types import pk_id
from src.models.base import Base


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[pk_id]
    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id', ondelete='CASCADE'))
    courier_id: Mapped[int] = mapped_column(ForeignKey('couriers.id'))
    pickup_address: Mapped[str]
    delivery_address: Mapped[str]
    delivery_fee: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    accepted_at: Mapped[datetime] = mapped_column(default=datetime.now())
    delivered_at: Mapped[datetime] = mapped_column(default=datetime.now())
