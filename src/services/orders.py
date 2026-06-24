from typing import Any, Coroutine

from fastapi import HTTPException
from sqlalchemy import select, and_, Select
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from src.models import Orders
from src.shemas.order import OrderSchema
from datetime import datetime, timezone

from src.shemas.response import Response_message_Schema

order_not_found = HTTPException(status_code=404, detail="Order not found")

server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='an error has occurred on the server please try again'
)


async def orders(
        smtp: Select,
        session: AsyncSession
) -> list[OrderSchema]:
    result = await session.scalars(smtp)
    result = [OrderSchema.from_orm(item) for item in result]
    if result:
        return result
    raise order_not_found


async def accepted_or_delivered_at(
        session: AsyncSession,
        order_id: int,
        courier_id: int,
        type: str
):
    smtp = select(Orders).filter_by(id=order_id, courier_id=courier_id)
    try:
        result = await session.scalar(smtp)
        if result is None:
            raise order_not_found
        if type == 'accepted_at':
            result.accepted_at = datetime.now(tz=timezone.utc)
        if type == 'delivered_at':
            result.delivered_at = datetime.now(tz=timezone.utc)
        await session.commit()
    except Exception as err:
        await session.rollback()
        raise server_error


async def get_pending_orders(session: AsyncSession) -> list[OrderSchema]:
    smtp = select(Orders).filter_by(courier_id=None, accepted_at=None, delivered_at=None)

    result = await session.scalars(smtp)
    orders = [OrderSchema.from_orm(item) for item in result]
    if orders:
        return orders
    raise order_not_found


async def accept_order_(
        session: AsyncSession,
        order_id: int,
        courier_id: int,
):
    smtp = select(Orders).filter_by(id=order_id).with_for_update()
    result = await session.scalar(smtp)
    if result.courier_id is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Someone else took the order")
    result.courier_id = courier_id
    await session.commit()
    return {'message': 'have you accepted the order'}


async def pickup_order_(
        session: AsyncSession,
        order_id: int,
        courier_id: int,
):
    await accepted_or_delivered_at(session, order_id, courier_id, 'accepted_at')
    return {'message': 'You received this order at the pick-up point'}


async def delivered_order_(
        session: AsyncSession,
        order_id: int,
        courier_id: int,
) -> dict[str, str]:
    await accepted_or_delivered_at(session, order_id, courier_id, 'delivered_at')
    return {'message': 'You received this order at the delivered point'}


async def cancel_order_(
        session: AsyncSession,
        order_id: int,
        courier_id: int,
) -> dict[str, str]:
    smtp = select(Orders).where(
        and_(Orders.id == order_id, Orders.courier_id == courier_id, Orders.accepted_at != None)
    )
    try:
        result = await session.scalar(smtp)
        if result is None:
            raise order_not_found
        result.accepted_at = None
        await session.commit()
        return {'message': 'You canceled this order'}

    except Exception as err:
        raise server_error


async def get_active_orders(
        session: AsyncSession,
        courier_id: int
):
    smtp = select(Orders).where(
        and_(
            Orders.courier_id == courier_id,
            Orders.accepted_at != None,
            Orders.delivery_fee == None,
        )
    )

    await orders(smtp, session)


async def get_my_orders(
        session: AsyncSession,
        courier_id: int
):
    smtp = select(Orders).where(
        and_(
            Orders.courier_id == courier_id,
            Orders.accepted_at != None,
            Orders.delivery_fee != None,
        )
    )
    await orders(smtp, session)
