from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from src.core.dependencies.depends import get_partner_id, get_partners
from src.database import get_session
from src.services.partners import (
    register_partners_,
    login_partners_,
    update_partnet,
)
from src.shemas.partner import RegisterPartnerSchema, LoginPartnerSchema, Api_Key_Schema, UpdatePartnerSchema

router = APIRouter(prefix='/api/v1')


@router.post('/partners/register', tags=['partners'])
async def register_partners(
        partner: RegisterPartnerSchema,
        session: AsyncSession = Depends(get_session)

) -> Api_Key_Schema:
    result = await register_partners_(session, partner.dict())
    return result


@router.post('/partners/login', tags=['partners'])
async def login(
        partner: LoginPartnerSchema,
        session: AsyncSession = Depends(get_session)
) -> Api_Key_Schema:
    result = await login_partners_(session, partner.dict())
    return result


@router.patch('/partners/me', tags=['partners'], status_code=status.HTTP_204_NO_CONTENT)
async def update_me(
        partner: UpdatePartnerSchema,
        contex: dict = Depends(get_partners)
):
    result = await update_partnet(contex, partner.dict())
    return result
