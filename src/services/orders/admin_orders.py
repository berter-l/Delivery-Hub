from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Orders
from src.services.orders.orders import order_not_found
from src.services.paginate import paginate
from src.shemas.order import ViewOrderSchema


async def filter_orders_(
        filters: dict,
        session: AsyncSession,
        paginate_: dict
) -> list[ViewOrderSchema]:
    new_filters = {key: filters[key] for key in filters if filters[key] is not None}

    smtp = select(Orders).filter_by(**new_filters)
    smtp = await paginate(smtp, paginate_, Orders)
    result = await session.scalars(smtp)
    result = [ViewOrderSchema.from_orm(obj) for obj in result]
    if not result:
        raise order_not_found
    return result
