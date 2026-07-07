from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Orders
from src.models import Admins
from src.services.couriers import check_password_get_token
from src.services.orders.orders import order_not_found
from src.shemas.order import ViewOrderSchema
from src.shemas.token import Get_token_Shema


async def login_admin(
        session: AsyncSession,
        login: dict
) -> Get_token_Shema:
    smtp = select(Admins).filter_by(email=login['email'])
    result = await check_password_get_token(smtp, session, login['password'])
    return Get_token_Shema(**result)


