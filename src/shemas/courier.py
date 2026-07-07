from typing import Annotated

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

Phone_Number = Annotated[PhoneNumber, PhoneNumberValidator(default_region='RU', number_format="E164",
                                                           supported_regions=['RU'])]


class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    phone: Phone_Number
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class Get_profile_Shema(BaseModel):
    first_name: str
    last_name: str
    phone: Phone_Number
    email: EmailStr
    rating: float
    balance: float
    total_deliveries: int
    model_config = ConfigDict(from_attributes=True)


class View_Couriers_Schema(BaseModel):
    first_name: str
    last_name: str
    phone: Phone_Number
    email: EmailStr
    balance: float
    model_config = ConfigDict(from_attributes=True)