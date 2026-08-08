from enum import Enum
from random import randint

from pydantic import BaseModel, Field


def random_value():
    return randint(1000, 5000)


class Shipment(BaseModel):
    content: str = Field(max_length=25)
    weight: float = Field(description="Weight of shipment is in (kgs)", le=25, ge=1)
    status: str
    code: int | None = Field(default_factory=random_value)

class ShipmentStatus(str,Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"
    cancelled = "cancelled"


class ShipmentStatusUpdate(BaseModel):
    status : ShipmentStatus
