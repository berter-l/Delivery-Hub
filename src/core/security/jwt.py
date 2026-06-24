import asyncio
from datetime import datetime, timezone, timedelta

import jwt
from fastapi import HTTPException
from starlette import status

from src.core.config import settings

key = settings.jwt.JWT_SECRET_KEY
invalid_jwt = HTTPException(
    detail="The token is invalid. Please log in again.",
    status_code=status.HTTP_401_UNAUTHORIZED,
)
exp_jwt = HTTPException(
    detail="The token is expired. Please log in again.",
    status_code=status.HTTP_401_UNAUTHORIZED,
)


async def get_jwt_token(courier_id: int) -> dict[str, str]:
    access_token = await asyncio.to_thread(
        jwt.encode,
        {
            "id": courier_id,
            "exp": datetime.now(tz=timezone.utc)
            + timedelta(minutes=settings.jwt.Exp_access),
        },
        key,
        algorithm=settings.jwt.JWT_ALGORITHM,
    )
    refresh_token = await asyncio.to_thread(
        jwt.encode,
        {
            "id": courier_id,
            "exp": datetime.now(tz=timezone.utc)
            + timedelta(minutes=settings.jwt.Exp_refresh),
            "refresh": True
        },
        key,
        algorithm=settings.jwt.JWT_ALGORITHM,
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


async def decode_jwt_token(token: str) -> dict | None:
    try:
        data = await asyncio.to_thread(
            jwt.decode, token, key, settings.jwt.JWT_ALGORITHM
        )
        return data
    except jwt.ExpiredSignatureError:
        raise exp_jwt
    except jwt.InvalidTokenError:
        raise invalid_jwt


async def update_jwt_token(refresh: str) -> dict[str, str]:
    try:
        data = await decode_jwt_token(refresh)
        if data.get("refresh") is None:
            raise invalid_jwt
        new_tokens = await get_jwt_token(data["id"])
        return new_tokens

    except jwt.ExpiredSignatureError:
        raise exp_jwt
    except jwt.InvalidTokenError:
        raise invalid_jwt
