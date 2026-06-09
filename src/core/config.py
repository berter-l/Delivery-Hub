from pydantic_settings import BaseSettings

from src.core.db_conf import DBconfig


class Settings(BaseSettings):
    db: DBconfig = DBconfig()


settings = Settings()
