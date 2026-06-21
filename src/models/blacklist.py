from sqlalchemy.orm import Mapped

from src.models.base import Base


class Token_blacklist(Base):
    __tablename__ = 'blacklist'

    token: Mapped[str]
