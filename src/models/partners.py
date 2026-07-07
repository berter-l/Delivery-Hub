from typing import Annotated

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, Roles

unique_null = Annotated[str, mapped_column(unique=True, nullable=False)]


class Partners(Base):
    __tablename__ = "partners"

    name: Mapped[str]
    api_key: Mapped[unique_null]
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    email: Mapped[unique_null]
    phone: Mapped[unique_null]
    contact_name: Mapped[unique_null]
    address: Mapped[unique_null]
    role: Mapped[Roles] = mapped_column(Enum(Roles))
