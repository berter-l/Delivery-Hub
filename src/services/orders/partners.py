import logging

from fastapi import HTTPException
from sqlalchemy import select

from src.models import Orders
from src.services.orders.orders import orders, server_error, order_not_found
from src.services.paginate import paginate
from src.shemas.order import ViewOrderSchema

logger = logging.getLogger('app')


async def create_order_(
        order: dict,
        partner: dict
):
    session = partner["session"]
    order['partner_id'] = partner['partners'].id
    order['status'] = 'PENDING'
    try:
        order_object = Orders(**order)
        session.add(order_object)
        await session.commit()
    except Exception as e:
        logger.exception(str(e))
        await session.rollback()
        raise server_error


async def get_orders_(context: dict, paginate_parameters: dict) -> list[ViewOrderSchema]:
    smtp = select(Orders).filter_by(partner_id=context["partners"].id)
    smtp = await paginate(smtp, paginate_parameters, Orders)
    result = await orders(smtp, context['session'])
    return result


async def delete_order_(
        order_id: int,
        context: dict
) -> dict:
    session = context["session"]
    smtp = select(Orders).filter_by(id=order_id)
    try:
        result = await session.scalar(smtp)
        if result.partner_id != context["partner_id"]:
            raise HTTPException(status_code=400, detail="you are not the owner of this order.")
        if result is None:
            raise order_not_found
        if result.accepted_at is not None:
            raise HTTPException(status_code=400, detail="You cannot delete this order because it has already been "
                                                        "accepted")

        session.delete(result)
        await session.commit()

    except Exception as e:
        logger.exception(str(e))
        await session.rollback()
        raise server_error
