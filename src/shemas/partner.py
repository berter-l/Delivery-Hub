from pydantic import BaseModel, EmailStr, ConfigDict

from src.shemas.courier import Phone_Number


class RegisterPartnerSchema(BaseModel):
    name: str
    email: EmailStr
    phone: Phone_Number
    contact_name: str
    address: str


class Api_Key_Schema(BaseModel):
    api_key: str


class LoginPartnerSchema(BaseModel):
    email: EmailStr
    phone: Phone_Number


class UpdatePartnerSchema(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    phone: Phone_Number | None = None
    address: str | None = None


class ViewPartnerSchema(BaseModel):
    email: EmailStr
    name: str
    contact_name: str
    address: str
    model_config = ConfigDict(from_attributes=True)
