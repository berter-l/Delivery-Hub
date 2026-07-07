from pathlib import Path

from pydantic import BaseModel

DB_DIR = Path(__file__).parent.parent / 'dbname.db'


class DBconfig(BaseModel):
    ECHO: bool = False
    DB_USER: str = 'fastapi_test'
    DB_PASSWORD: str = '1234'
    DB_HOST: str = "postgres_test"
    DB_PORT: int = 5432
    DB_NAME: str = "delivery_hub"

    @property
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
