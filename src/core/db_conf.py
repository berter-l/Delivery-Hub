from pydantic import BaseModel


class DBconfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    echo: bool = False