from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.depends.depends import get_courier, get_courier_id, get_access_tokens
from src.database import get_session
from src.models import Couriers
from src.services.couriers import (
    register_couriers_,
    login_couriers_,
    get_courier_profile,
    get_courier_orders,
    courier_logout_,
)
from src.shemas.courier import RegisterSchema, LoginSchema, Get_profile_Shema
from src.shemas.order import OrderSchema
from src.shemas.token import Get_token_Shema

router = APIRouter(prefix='/api/v1')


@router.post("/couriers/register", tags=["couriers"])
async def register_couriers(
        courier: RegisterSchema,
        db: AsyncSession = Depends(get_session)
) -> Get_token_Shema:
    result = await register_couriers_(db, courier.dict())
    return result


@router.post("/couriers/login", tags=["couriers"])
async def login_couriers(
        courier: LoginSchema,
        session: AsyncSession = Depends(get_session)
) -> Get_token_Shema:
    result = await login_couriers_(session, courier.dict())
    return result


@router.get('/couriers/me', tags=["couriers"])
async def courier_me(
        courier: Couriers = Depends(get_courier)
) -> Get_profile_Shema:
    result = await get_courier_profile(courier)
    return result


@router.get('/couriers/me/orders', tags=["couriers"])
async def courier_me_orders(
        courier_id: int = Depends(get_courier_id),
        session: AsyncSession = Depends(get_session)
) -> list[OrderSchema]:
    result = await get_courier_orders(session, courier_id)
    return result


@router.post('/couriers/logout', tags=["couriers"])
async def courier_logout(
        refresh_token: str,
        courier_id: int = Depends(get_courier_id),
        session: AsyncSession = Depends(get_session)

):
    result = await courier_logout_(session, courier_id, refresh_token)
    return result
