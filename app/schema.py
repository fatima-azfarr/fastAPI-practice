from enum import Enum

from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"
    cancelled = "cancelled"

# to get better understanding of response models
# they’re structures that define what shape the system’s output should have

class BaseShipment(BaseModel):
    content: str = Field(max_length=25)
    weight: float = Field(description="Weight of shipment in (kgs)", le=25, ge=1)
    destination: str

# what the server stores internally and returns in every response
class ShipmentRead(BaseShipment):
    id : int
    status: ShipmentStatus

# what a client sends to POST (no status — server sets it to placed)
class ShipmentCreate(BaseShipment):
    pass

# what a client sends to PUT (full replace, including status)
class ShipmentUpdate(BaseShipment):
    status: ShipmentStatus

# what a client sends to PATCH (status only)
class ShipmentStatusUpdate(BaseModel):
    status: ShipmentStatus