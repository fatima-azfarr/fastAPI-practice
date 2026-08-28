from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .database import save, shipments
from .schema import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentStatusUpdate,
    ShipmentUpdate,
)

app = FastAPI()


@app.get("/shipments/{id}",response_model=ShipmentRead)
def read_shipment(id:int)->ShipmentRead:

    #check for id
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Invalid request,the given id #{id} doesn't exits!"
        )

    return shipments[id]


@app.post("/shipments", response_model=None)
# body:ShipmentCreate - fastapi validates the incoming json against shipmentCreate - (pydantic model validation)
def submit_shipment(body: ShipmentCreate):
    # generating new id and assigning to shipment
    new_id = max(shipments.keys()) + 1

    # body.model_dumps() - converts the pydantic model into python dictionary
    # **body.model_dumps() - unpacks the dictionary
    shipments[new_id] = {
        **body.model_dump(),
        "id" : new_id,
        "status" : ShipmentStatus.placed
    }
    save()
    return {"id": new_id}


@app.put("/shipments/{id}",response_model=ShipmentRead)
def update_shipment(id:int,body:ShipmentUpdate)->ShipmentRead:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Invalid request, the given id #{id} doesn't exits!"
            )
    shipments[id] = {
        "id" : id,
        **body.model_dump(),
    }
    save()
    return shipments[id]


@app.patch("/shipments/{id}",response_model=ShipmentRead)
def patch_shipment(id:int,body:ShipmentStatusUpdate):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Invalid request, the given id #{id} doesn't exits!"
        )
    shipments[id]["status"] = body.status
    save()
    return shipments[id]

@app.delete("/shipments/{id}")
def delete_shipment(id:int)->dict[str,str]:
    if id not in shipments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Invalid request, the given id #{id} doesn't exits!"
            )
    shipments.pop(id)
    save()

    return {
        "details" : f"The given id #{id} is deleted."
    }

@app.get("/scalar", include_in_schema=False)
def scalar_documentation():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="scalar API")