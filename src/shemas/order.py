from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderSchema(BaseModel):
    pickup_address: str
    delivery_address: str
    accepted_at: datetime
    delivered_at: datetime
    delivery_fee: float
    model_config = ConfigDict(from_attributes=True)


