import logging
import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Partners
from src.services import partner_not_found
from src.services.orders.orders import server_error
from src.shemas.partner import Api_Key_Schema, ViewPartnerSchema

logger = logging.getLogger('app')


async def register_partners_(
        session: AsyncSession,
        partner: dict
) -> Api_Key_Schema:
    partner['role'] = 'PARTNER'
    partner['api_key'] = str(uuid.uuid4())
    try:
        partner_object = Partners(**partner)
        session.add(partner_object)
        await session.commit()
        return Api_Key_Schema(api_key=partner['api_key'])

    except Exception as e:
        logger.exception(str(e))
        await session.rollback()

        raise server_error


async def login_partners_(
        session: AsyncSession,
        login_partner: dict
) -> Api_Key_Schema:
    smtp = select(Partners).where(
        and_(Partners.email == login_partner['email'], Partners.phone == login_partner['phone']))
    try:
        result = await session.scalar(smtp)
        if result is None:
            raise partner_not_found
        new_api_key = str(uuid.uuid4())
        result.api_key = new_api_key
        await session.commit()
        return Api_Key_Schema(api_key=new_api_key)
    except Exception as e:
        logger.exception(str(e))
        await session.rollback()
        raise server_error


async def update_partnet(
        context: dict,
        new_data: dict
):
    session = context["session"]
    try:
        for x in new_data:
            if new_data[x] is not None:
                setattr(context["partners"], x, new_data[x])
        await session.commit()
    except Exception as e:
        logger.exception(str(e))
        await session.rollback()
        raise server_error


async def get_not_approve_partners_(
        session: AsyncSession
) -> list[ViewPartnerSchema]:
    smtp = select(Partners).filter_by(is_active=False)

    result = await session.scalars(smtp)
    result = [ViewPartnerSchema.from_orm(obj) for obj in result]
    return result


async def approve_(
        cls,
        id: int,
        session: AsyncSession
):
    smtp = select(cls).filter_by(id=id)
    try:
        result = await session.scalar(smtp)
        if result is None:
            raise partner_not_found
        result.is_active = True
        await session.commit()

    except Exception as e:
        logger.exception(str(e))
        await session.rollback()
        raise server_error
