import logging
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.core.security.jwt import decode_jwt_token, invalid_jwt
from src.database import get_session
from src.models import Couriers, Partners
from src.models.base import Status
from src.services import partner_not_found
from src.models import Admins
from src.shemas.pagination import PaginateSchema

security = HTTPBearer()

activate_error = HTTPException(status_code=400, detail="You cannot perform any actions until your account is activated")


async def get_object(
        cls,
        token: str,
        session: AsyncSession,

):
    result = await decode_jwt_token(token)
    if result.get('refresh') is not None:
        raise invalid_jwt
    id = result.get("id")
    if not isinstance(id, int):
        smtp = select(Admins).filter_by(id=id)
        object = await session.scalar(smtp)
        return object
    else:
        smtp = select(Couriers).filter_by(id=id)
        object = await session.scalar(smtp)
    return object


async def get_courier(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        session: AsyncSession = Depends(get_session),
) -> Couriers | None:
    couriers = await get_object(Couriers, credentials.credentials, session)
    if couriers is None:
        raise HTTPException(status_code=404, detail="Courier not found")
    if not couriers.is_active:
        raise activate_error
    return couriers


async def get_courier_id(
        courier: Couriers = Depends(get_courier),
) -> int:
    id_courier = courier.id
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


async def get_partner_context(
        api_key: str = Header(alias='X-API-KEY'),
        session: AsyncSession = Depends(get_session)
) -> dict:
    smtp = select(Partners).filter_by(api_key=api_key)
    result = await session.scalar(smtp)
    if result is None:
        raise partner_not_found
    if not result.is_active:
        raise activate_error
    return {'partner': result, 'session': session}


async def get_partner_id(
        context: dict = Depends(get_partner_context),
) -> dict:
    return {'id': context['partner'].id, 'session': context['session']}


async def get_partners(
        context: dict = Depends(get_partner_context),
) -> dict:
    return {'partners': context['partner'], 'session': context['session']}


async def filter_(
        status: Status | None = None,
        partner_id: int | None = None,
        courier_id: int | None = None
):
    filters = {"status": status, "courier_id": courier_id, "partner_id": partner_id}
    return filters


async def get_admin(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        session: AsyncSession = Depends(get_session),
):
    admin = await get_object(Admins, credentials.credentials, session)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


async def paginate(
        parameters: PaginateSchema = Depends()
) -> dict:
    return {'page': parameters.page, 'size': parameters.size}
