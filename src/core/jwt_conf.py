import uuid

from pydantic import BaseModel


class JwtConfig(BaseModel):
    JWT_SECRET_KEY: str = 'Kxc3xW0PPGOfRuhU2pMoIluW8bw4w_1MZTDNBDq5P673wzxeMC9AUHxLE6lg0STJwO0'
    JWT_ALGORITHM: str = 'HS256'
    Exp_access: int = 10
    Exp_refresh: int = 5 * 24 * 60
