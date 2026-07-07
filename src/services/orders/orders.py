from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select, and_, Select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.models import Orders, Couriers
from src.shemas.order import ViewOrderSchema

order_not_found = HTTPException(status_code=404, detail="Order not found")

server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='an error has occurred on the server please try again'
)


async def orders(
        smtp: Select,
        session: AsyncSession
) -> list[ViewOrderSchema]:
    result = await session.scalars(smtp)
    result = [ViewOrderSchema.from_orm(item) for item in result]
    if result:
        return result
    raise order_not_found







