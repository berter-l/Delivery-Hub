from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.core.security.hache import get_hashed_password, check_hashed_password
from src.core.security.jwt import get_jwt_token
from src.models import Couriers
from src.models.blacklist import Token_blacklist
from src.shemas.courier import Get_profile_Shema
from src.shemas.order import OrderSchema

not_found_email_password = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Courier with email  email not found or  password  not found.",
)


async def register_couriers_(
        session: AsyncSession,
        courier: dict
):
    try:
        password_hash = await get_hashed_password(courier.pop("password"))
        courier["password_hash"] = password_hash
        courier["fcm_token"] = ""
        courier = Couriers(**courier)
        session.add(courier)

        await session.flush()
        id_user = courier.id
        tokens = await get_jwt_token(id_user)
        await session.commit()
        return tokens
    except Exception:
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
    result = await session.scalars(smtp)
    result = result.all()
    if not result:
        raise not_found_email_password
    check_password = await check_hashed_password(
        result[0].password_hash, courier["password"].encode()
    )
    if check_password:
        tokens = await get_jwt_token(result[0].id)
        return tokens
    raise not_found_email_password


async def get_courier_profile(courier: Couriers) -> Get_profile_Shema:
    profile = Get_profile_Shema.from_orm(courier)
    return profile


async def get_courier_orders(
        session: AsyncSession,
        id: int
) -> list[OrderSchema]:
    smtp = select(Couriers).options(selectinload(Couriers.orders)).filter_by(id=id)
    result = await session.scalar(smtp)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Courier with id {id} not found.")

    result = [OrderSchema.from_orm(q) for q in result.orders]
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='order not found.')
    return result


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
