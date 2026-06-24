from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from src.core.depends.depends import get_courier_id, get_order_context
from src.database import get_session
from src.services.orders import (
    get_pending_orders,
    accept_order_,
    pickup_order_,
    delivered_order_,
    cancel_order_,
    get_active_orders,
    get_my_orders,
)
from src.shemas.order import OrderSchema
from src.shemas.response import Response_message_Schema

router = APIRouter(prefix='/api/v1')


@router.get('/orders/pending', tags=['orders'])
async def pending_orders(
        courier_id: int = Depends(get_courier_id),
        session: AsyncSession = Depends(get_session)
) -> list[OrderSchema]:
    result = await get_pending_orders(session)
    return result


@router.post('/orders/{order_id}/', tags=['orders'])
async def accept_order(
        contex: dict = Depends(get_order_context)
):
    result = await accept_order_(contex['session'], contex['order_id'], contex['courier_id'])
    return result


@router.patch('/orders/{order_id}/pickup', tags=['orders'], status_code=status.HTTP_200_OK)
async def pickup_order(
        contex: dict = Depends(get_order_context)
) -> Response_message_Schema:
    result = await pickup_order_(contex['session'], contex['order_id'], contex['courier_id'])
    return result


@router.patch('/orders/{order_id}/deliver', tags=['orders'], status_code=status.HTTP_200_OK)
async def deliver_order(
        contex: dict = Depends(get_order_context)
) -> Response_message_Schema:
    result = await delivered_order_(contex['session'], contex['order_id'], contex['courier_id'])
    return result


@router.patch('/orders/{order_id}/cancel', tags=['orders'], status_code=status.HTTP_200_OK)
async def cancel_order(
        contex: dict = Depends(get_order_context)
) -> Response_message_Schema:
    result = await cancel_order_(contex['session'], contex['order_id'], contex['courier_id'])

    return result


@router.get('/couriers/me/active_orders', tags=['orders'], status_code=status.HTTP_200_OK)
async def active_orders(
        session: AsyncSession = Depends(get_session),
        courier_id: int = Depends(get_courier_id)
) -> list[OrderSchema]:
    result = await get_active_orders(session, courier_id)
    return result


@router.get('/couriers/me/orders', tags=['orders'], status_code=status.HTTP_200_OK)
async def my_orders(
        session: AsyncSession = Depends(get_session),
        courier_id: int = Depends(get_courier_id)

):
    result = await get_my_orders(session, courier_id)
    return result
