import logging

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from src.core.config import settings
from src.core.dependencies.depends import (
    get_courier_id,
    get_order_context,
    paginate,
    filter_,
    get_admin,
    get_partner_id,
    get_partners,
)
from src.database import get_session
from src.models import Admins
from src.services.orders.admin_orders import filter_orders_
from src.services.orders.couriers_order import (
    get_pending_orders,
    accept_order_,
    pickup_order_,
    delivered_order_,
    cancel_order_,
    get_active_orders,
    get_courier_orders,
)
from src.services.orders.partners import get_orders_, create_order_, delete_order_
from src.shemas.order import ViewOrderSchema, CreateOrderSchema
from src.shemas.response import Response_message_Schema

router = APIRouter(prefix='/api/v1')


@router.get('/orders/courier/pending', tags=['orders-courier'])
async def pending_orders(
        courier_id: int = Depends(get_courier_id),
        session: AsyncSession = Depends(get_session),
        paginate_=Depends(paginate)
) -> list[ViewOrderSchema]:
    result = await get_pending_orders(session, paginate_)
    return result


@router.post('/orders/courier/{order_id}/accept', tags=['orders-courier'])
async def accept_order(
        contex: dict = Depends(get_order_context)
):
    result = await accept_order_(contex['session'], contex['order_id'], contex['courier_id'])
    return result


@router.patch('/orders/courier/{order_id}/pickup', tags=['orders-courier'], status_code=status.HTTP_200_OK)
async def pickup_order(
        contex: dict = Depends(get_order_context)
) -> Response_message_Schema:
    result = await pickup_order_(contex['session'], contex['order_id'], contex['courier_id'])
    return result


@router.patch('/orders/courier/{order_id}/deliver', tags=['orders-courier'], status_code=status.HTTP_200_OK)
async def deliver_order(
        contex: dict = Depends(get_order_context)
) -> Response_message_Schema:
    result = await delivered_order_(contex['session'], contex['order_id'], contex['courier_id'])
    return result


@router.patch('/orders/courier/{order_id}/cancel', tags=['orders-courier'], status_code=status.HTTP_200_OK)
async def cancel_order(
        contex: dict = Depends(get_order_context)
) -> dict[str, str]:
    result = await cancel_order_(contex['session'], contex['order_id'], contex['courier_id'])

    return result


@router.get('/orders/courier/me', tags=['orders-courier'], status_code=status.HTTP_200_OK)
async def active_orders(
        session: AsyncSession = Depends(get_session),
        courier_id: int = Depends(get_courier_id),
        paginate_=Depends(paginate)
) -> list[ViewOrderSchema]:
    result = await get_active_orders(session, courier_id, paginate_)
    return result


@router.get('/orders/courier', tags=["orders-courier"])
async def courier_me_orders(
        courier_id: int = Depends(get_courier_id),
        session: AsyncSession = Depends(get_session),
        paginate_=Depends(paginate)
) -> list[ViewOrderSchema]:
    result = await get_courier_orders(session, courier_id, paginate_)
    return result


@router.get('/orders/admin', tags=['orders-admin'])
async def filter_orders(
        filter_data: dict = Depends(filter_),
        session: AsyncSession = Depends(get_session),
        admin: Admins = Depends(get_admin),
        paginate_=Depends(paginate)
):
    result = await filter_orders_(filter_data, session,paginate_)
    return result


@router.delete('/orders/partner/{order_id}', tags=['orders-partner'])
async def delete_order(
        response: Response,
        order_id: int,
        contex: dict = Depends(get_partner_id),
):
    result = await delete_order_(order_id, contex)
    response.status_code = status.HTTP_204_NO_CONTENT
    return result


@router.get('/orders/partner', tags=['orders-partner'])
async def get_partner_orders(
        contex: dict = Depends(get_partners),
        paginate_parameters: dict = Depends(paginate)
) -> list[ViewOrderSchema]:
    result = await get_orders_(contex, paginate_parameters)
    return result


@router.post('/orders/partner', tags=['orders-partner'])
async def create_orders(
        order: CreateOrderSchema,
        contex: dict = Depends(get_partners)
):
    result = await create_order_(order.dict(), contex)
    return result


