import logging
from datetime import timezone, datetime

from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.models import Couriers, Orders
from src.services.couriers import not_found_couriers
from src.services.orders.orders import (
    order_not_found,
    server_error,
    orders,
)
from src.services.paginate import paginate
from src.shemas.order import ViewOrderSchema

logger = logging.getLogger('app')

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


async def get_courier_orders(
        session: AsyncSession,
        id: int,
        paginate_params: dict,
) -> list[ViewOrderSchema]:
    smtp = select(Orders).filter_by(courier_id=id)
    smtp = await paginate(smtp, paginate_params, Orders)
    result = await session.scalars(smtp)
    if result is None:
        raise not_found_couriers

    result = [ViewOrderSchema.from_orm(q) for q in result]
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='order not found.')
    return result


async def cancel_order_(
        session: AsyncSession,
        order_id: int,
        courier_id: int,
) -> dict[str, str]:
    smtp = select(Orders).where(
        and_(Orders.id == order_id, Orders.courier_id == courier_id, Orders.accepted_at != None,
             Orders.delivered_at == None)
    )
    try:
        result = await session.scalar(smtp)
        if result is None:
            raise order_not_found
        result.accepted_at = None
        result.courier_id = None
        result.status = 'PENDING'
        await session.commit()
        return {'message': 'You canceled this order'}

    except Exception as err:
        logger.exception(str(err))
        raise server_error


async def get_active_orders(
        session: AsyncSession,
        courier_id: int,
        paginate_parameters: dict,
):
    smtp = select(Orders).where(
        and_(
            Orders.courier_id == courier_id,
            Orders.accepted_at != None,
            Orders.delivered_at == None,
        )
    )
    smtp = await paginate(smtp, paginate_parameters, Orders)
    result = await orders(smtp, session)
    return result


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
    result = await orders(smtp, session)
    return result


async def accept_order_(
        session: AsyncSession,
        order_id: int,
        courier_id: int,
):
    try:
        smtp = select(Orders).filter_by(id=order_id).with_for_update()
        result = await session.scalar(smtp)
        if result is None:
            raise order_not_found
        if result.courier_id is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Someone else took the order")

        result.courier_id = courier_id
        result.status = 'ACCEPTED'
        await session.commit()
        return {'message': 'have you accepted the order'}

    except Exception as err:
        logger.exception(str(err))
        await session.rollback()
        raise server_error


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
            result.status = 'DELIVERED'
        await session.commit()
    except Exception as err:
        logger.exception(str(err))
        await session.rollback()
        raise server_error


async def get_pending_orders(session: AsyncSession, paginate_parameters: dict) -> list[ViewOrderSchema]:
    smtp = select(Orders).filter_by(courier_id=None, accepted_at=None, delivered_at=None)
    smtp = await paginate(smtp, paginate_parameters, Orders)
    result = await session.scalars(smtp)
    orders = [ViewOrderSchema.from_orm(item) for item in result]
    if orders:
        return orders
    raise order_not_found
