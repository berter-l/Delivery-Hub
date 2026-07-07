from typing import Any, Coroutine

from fastapi import APIRouter, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.core.dependencies.depends import filter_, get_admin, paginate
from src.core.security.hache import get_hashed_password
from src.database import get_session
from src.models import Partners, Couriers, Admins
from src.services.admin import login_admin
from src.services.couriers import get_couriers_
from src.services.partners import get_not_approve_partners_, approve_
from src.shemas.admin import LoginAdminSchema
from src.shemas.courier import View_Couriers_Schema
from src.shemas.order import ViewOrderSchema
from src.shemas.partner import ViewPartnerSchema
from src.shemas.token import Get_token_Shema

router = APIRouter(prefix='/api/v1')


@router.post('/admin/login', tags=['admin'])
async def login(
        login: LoginAdminSchema,
        session: AsyncSession = Depends(get_session)
) -> Get_token_Shema:
    result = await login_admin(session, login.dict())
    return result


@router.get('/admin/orders', tags=['admin'])
async def filter_orders(
        filter_data: dict = Depends(filter_),
        session: AsyncSession = Depends(get_session),
        admin: Admins = Depends(get_admin)
):
    result = await filter_orders(filter_data, session)
    return result


@router.get('/partners', tags=['admin'])
async def get_not_approve_partners(
        session: AsyncSession = Depends(get_session),
        admin: Admins = Depends(get_admin),
) -> list[ViewPartnerSchema]:
    result = await get_not_approve_partners_(session)
    return result


@router.post('/admin/partners/{partner_id}/approve', tags=['admin'])
async def approve(
        partner_id: int,
        response: Response,
        session: AsyncSession = Depends(get_session),
        admin: Admins = Depends(get_admin)
):
    result = await approve_(Partners, partner_id, session)
    response.status_code = status.HTTP_204_NO_CONTENT
    return result


@router.get('/admin/couriers', tags=['admin'])
async def get_couriers(
        is_active: bool | None = None,
        session: AsyncSession = Depends(get_session),
        admin: Admins = Depends(get_admin),
        paginate_parameters: dict = Depends(paginate)
) -> list[View_Couriers_Schema]:
    result = await get_couriers_(is_active, session,paginate_parameters)

    return result


@router.post('/admin/couriers/{courier_id}/approve', tags=['admin'])
async def approve_courier(
        courier_id: int,
        response: Response,
        session: AsyncSession = Depends(get_session),
        admin: Admins = Depends(get_admin)
):
    result = await approve_(Couriers, courier_id, session)
    response.status_code = status.HTTP_204_NO_CONTENT
    return result


@router.post('register/')
async def register(
        email,
        password,
        first_name,
        last_name,
        session: AsyncSession = Depends(get_session)
):
    new_password = await get_hashed_password(password)
    admin = Admins(email=email, password_hash=new_password, first_name=first_name, last_name=last_name, role='ADMIN')
    session.add(admin)
    await session.commit()
