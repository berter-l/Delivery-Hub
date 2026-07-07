import logging
import uuid

from fastapi import HTTPException
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.util import await_only
from starlette import status

from src.core.config import settings
from src.core.security.hache import get_hashed_password, check_hashed_password
from src.core.security.jwt import get_jwt_token
from src.models import Couriers
from src.models.blacklist import Token_blacklist
from src.services.paginate import paginate
from src.services.partners import approve_
from src.shemas.courier import Get_profile_Shema, View_Couriers_Schema
from src.shemas.order import ViewOrderSchema
logger = logging.getLogger("app")
not_found_email_password = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Courier with email  email not found or  password  not found.",
)

not_found_couriers = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Couriers not found.",
)


async def register_couriers_(
        session: AsyncSession,
        courier: dict
):
    try:
        password_hash = await get_hashed_password(courier.pop("password"))
        courier["password_hash"] = password_hash
        courier["fcm_token"] = str(uuid.uuid4())
        courier['role'] = 'ADMIN'
        courier = Couriers(**courier)
        session.add(courier)

        await session.flush()
        id_user = courier.id
        tokens = await get_jwt_token(id_user)
        await session.commit()
        return tokens
    except Exception as e:
        logger.exception(str(e))

        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='an error has occurred, please try again later'
        )


async def login_couriers_(
        session: AsyncSession,
        courier: dict
):
    smtp = select(Couriers).filter_by(email=courier["email"])
    result = await check_password_get_token(smtp, session, courier["password"])
    return result


async def get_courier_profile(courier: Couriers) -> Get_profile_Shema:
    profile = Get_profile_Shema.from_orm(courier)
    return profile


async def courier_logout_(
        session: AsyncSession,
        id: int,
        refresh_token: str
):
    smtp = select(Couriers).filter_by(id=id)
    courier = await session.scalar(smtp)
    courier.is_active = False
    blacklist = Token_blacklist(token=refresh_token)
    session.add(blacklist)
    await session.commit()

    return {
        'message': 'courier logged out',
    }


async def check_password_get_token(
        smtp: Select,
        session: AsyncSession,
        password: str
):
    result = await session.scalar(smtp)
    if result is None:
        raise not_found_email_password
    check_password = await check_hashed_password(
        result.password_hash, password.encode()
    )
    if check_password:
        id = result.id
        if not isinstance(id, int):
            id = str(result.id)
        tokens = await get_jwt_token(id)
        return tokens
    raise not_found_email_password


async def get_couriers_(
        is_active: bool | None,
        session: AsyncSession,
        paginate_parameters: dict
) -> list[View_Couriers_Schema]:
    smtp = select(Couriers)
    if is_active is not None:
        smtp = smtp.filter_by(is_active=is_active)
    smtp = await paginate(smtp, paginate_parameters, Couriers)
    couriers = await session.scalars(smtp)
    result = [View_Couriers_Schema.from_orm(obj) for obj in couriers]
    if not result:
        raise not_found_couriers
    return result


async def approve_courier(
        courier_id: int,
        session: AsyncSession
):
    result = await approve_(Couriers, courier_id, session)
    return result
