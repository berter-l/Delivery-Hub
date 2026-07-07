from pydantic import BaseModel, PositiveInt


class PaginateSchema(BaseModel):
    size: PositiveInt = 2
    page: PositiveInt = 1
