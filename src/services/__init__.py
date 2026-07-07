from fastapi import HTTPException
from starlette import status

partner_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Partner not found')