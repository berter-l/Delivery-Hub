import starlette
from pydantic import BaseModel


class Response_message_Schema(BaseModel):
    message: str