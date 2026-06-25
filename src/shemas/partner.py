from pydantic import BaseModel, EmailStr


class RegisterPartnerSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    contact_name: str
    address: str
