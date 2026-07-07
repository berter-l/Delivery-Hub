from datetime import datetime
from enum import Enum
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.database import pk_id

default_type = Annotated[bool, mapped_column(default=False)]


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[pk_id]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Roles(Enum):
    ADMIN = 'admin'
    COURIER = 'courier'
    PARTNER = 'partner'


class Status(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    PICKUP = 'pickup'
    DELIVERED = 'delivered'
