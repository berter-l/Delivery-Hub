from pydantic import BaseModel


class Get_token_Shema(BaseModel):
    access_token: str
    refresh_token: str


class Update_Token(BaseModel):
    refresh_token: str

