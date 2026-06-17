from datetime import datetime, timezone, timedelta

from src.core.config import settings
from src.models import Couriers
import jwt
import asyncio

key = settings.jwt.JWT_SECRET_KEY


async def get_jwt_token(courier: int) -> dict[str, str]:
    access_token = await asyncio.to_thread(
        jwt.encode,
        {
            "id": courier,
            "exp": datetime.now(tz=timezone.utc)
            + timedelta(minutes=settings.jwt.Exp_access),
        },
        key,
        algorithm=settings.jwt.JWT_ALGORITHM,
    )
    refresh_token = await asyncio.to_thread(
        jwt.encode,
        {
            "exp": datetime.now(tz=timezone.utc)
            + timedelta(minutes=settings.jwt.Exp_refresh),
        },
        key,
        algorithm=settings.jwt.JWT_ALGORITHM,
    )

    return {"access_token": access_token, "refresh_token": refresh_token}
