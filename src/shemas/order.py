from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ViewOrderSchema(BaseModel):
    pickup_address: str
    delivery_address: str
    accepted_at: datetime | None
    delivered_at: datetime | None
    delivery_fee: float
    model_config = ConfigDict(from_attributes=True)
    description: str
    status: str


class CreateOrderSchema(BaseModel):
    pickup_address: str
    delivery_address: str
    description: str | None
    delivery_fee: float


