from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.core.security.jwt import decode_jwt_token, invalid_jwt
from src.database import get_session
from src.models import Couriers

security = HTTPBearer()


async def get_courier(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        session: AsyncSession = Depends(get_session),
) -> Couriers | None:

    result = await decode_jwt_token(credentials.credentials)
    if result.get("refresh"):
        raise invalid_jwt
    id_courier = result.get("id")

    smpt = select(Couriers).filter_by(id=id_courier)
    couriers = await session.scalar(smpt)
    if couriers is None:
        raise HTTPException(status_code=404, detail="Courier not found")
    return couriers


async def get_courier_id(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> int:
    result = await decode_jwt_token(credentials.credentials)
    id_courier = result.get("id")
    return id_courier


async def get_access_tokens(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    return credentials.credentials


async def get_order_context(
        order_id: int,
        session: AsyncSession = Depends(get_session),
        courier_id: int = Depends(get_courier_id)
):
    data = {}
    data["order_id"] = order_id
    data["session"] = session
    data["courier_id"] = courier_id
    return data
