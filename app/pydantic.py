from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schema import Shipment, ShipmentStatus, ShipmentStatusUpdate

app = FastAPI()


shipments = {
    12345: {"content": "wooden box", "weight": 20, "status": "in transit"},
    12346: {"content": "glassware", "weight": 10, "status": "placed"},
    12347: {"content": "mobile phones", "weight": 50, "status": "placed"},
    12348: {"content": "keyboard", "weight": 10, "status": "cancelled"},
}


# GET METHOD
@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
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
@app.post("/shipment")
def submit_shipments(body: Shipment) -> dict[str, Any]:

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = body.model_dump()
    return {"id": new_id}


# PUT METHOD
@app.put("/shipment/{id}")
def update_shipment(id: int, body: Shipment) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, the given id doesn't exist!",
        )

    shipments[id] = body.model_dump()
    return shipments[id]



# PATCH METHOD
# used body:dict[str,Any] to understand enums
@app.patch("/shipment")
def patch_shipment(id: int, body: ShipmentStatusUpdate) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, the given id doesn't exist!",
        )
    # updating data with given fields
    shipments[id]["status"] = body.status
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


# SCALAR API Documentation
@app.get("/scalar", include_in_schema=False)
def scalar_documentation():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="scalar API")
