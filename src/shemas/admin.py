from typing import Annotated

from pydantic import BaseModel, EmailStr, constr, StringConstraints

password_type = Annotated[str, StringConstraints(strip_whitespace=True, min_length=8, max_length=50)]


class LoginAdminSchema(BaseModel):
    email: EmailStr
    password: password_type
