import uuid

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import str_100
from src.models.base import Base, Roles


class Admins(Base):
    __tablename__ = 'admins'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[bytes]
    first_name: Mapped[str_100]
    last_name: Mapped[str_100]
    role: Mapped[Roles]
