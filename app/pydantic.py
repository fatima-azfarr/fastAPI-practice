from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schema import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentStatusUpdate,
    ShipmentUpdate,
)

app = FastAPI()


shipments: dict[int, ShipmentRead] = {
    12345: ShipmentRead(content="wooden box", weight=20, destination="Lahore", status=ShipmentStatus.in_transit),
    12346: ShipmentRead(content="glassware", weight=10, destination="Karachi", status=ShipmentStatus.placed),
    12347: ShipmentRead(content="mobile phones", weight=23, destination="Islamabad", status=ShipmentStatus.placed),
    12348: ShipmentRead(content="keyboard", weight=10, destination="Multan", status=ShipmentStatus.cancelled),
}


# GET METHOD
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int | None = None) -> ShipmentRead:
    if id is None:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, given id doesn't exist!",
        )
    return shipments[id]


# POST METHOD
@app.post("/shipment", response_model=ShipmentRead)
def submit_shipments(body: ShipmentCreate) -> ShipmentRead:
    new_id = max(shipments.keys()) + 1
    # here new_shipment basically contains the pydantic object
    new_shipment = ShipmentRead(**body.model_dump(), status=ShipmentStatus.placed)
    shipments[new_id] = new_shipment
    return new_shipment


# PUT METHOD
@app.put("/shipment/{id}", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate) -> ShipmentRead:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, the given id doesn't exist!",
        )
    shipments[id] = ShipmentRead(**body.model_dump())
    return shipments[id]


# PATCH METHOD
@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, body: ShipmentStatusUpdate) -> ShipmentRead:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, the given id doesn't exist!",
        )
    shipments[id].status = body.status
    return shipments[id]


# DELETE METHOD
@app.delete("/shipment/{id}")
def delete_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, the given id doesn't exist!",
        )
    deleted_shipment = shipments.pop(id)
    return {"detail": f"The shipment #{id} is deleted", "shipment": deleted_shipment}


@app.get("/scalar", include_in_schema=False)
def scalar_documentation():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="scalar API")