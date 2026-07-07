from pydantic_settings import BaseSettings

from .db_conf import DBconfig
from src.core.jwt_conf import JwtConfig
from src.core.log_conf import LogConfig


class Settings(BaseSettings):
    db: DBconfig = DBconfig()
    jwt: JwtConfig = JwtConfig()
    logs: LogConfig = LogConfig()


settings = Settings()
