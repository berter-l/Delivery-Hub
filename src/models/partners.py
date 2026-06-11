from sqlalchemy.orm import Mapped, mapped_column

from src.core.types import pk_id
from src.models.base import Base


class Partners(Base):
    __tablename__ = 'partners'

    id: Mapped[pk_id]
    name: Mapped[str]
    api_key: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool]
