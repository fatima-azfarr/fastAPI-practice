from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    12345: {"content": "wooden box", "weight": 20, "status": "in transit"},
    12346: {"content": "glassware", "weight": 10, "status": "placed"},
    12347: {"content": "mobile phones", "weight": 50, "status": "placed"},
    12348: {"content": "keyboard", "weight": 10, "status": "cancelled"},
}


# GET METHOD - (to get/fetch the existing data)
@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:

    if id is None:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, given id doesn't exits!",
        )

    else:
        return shipments[id]
    
    


# POST METHOD - (create or get new data from client to server)
@app.post("/shipment")
def submit_shipment(
    content: str, weight: float, shipment_status: str
) -> dict[str, int]:

    # validate the weight
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid Request, the weight exceeds the given limit (i.e 25 kgs)",
        )

    # create and assign shipment a new id
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": shipment_status,
    }
    return {"id": new_id}




# PUT METHOD - (updates all the existing data)
@app.put("/shipment/{id}")
def update_shipment(
    id: int, content: str, weight: float, shipment_status: str
) -> dict[str, Any]:

    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": shipment_status,
    }
    return shipments[id]



# PATCH METHOD - (updates certain fields of existing data)
@app.patch("/shipment")
def patch_shipment(
    # can be done as (id:int,body : dict[str,Any])
    id: int,
    content: str | None = None,
    weight: float | None = None,
    shipment_status: str | None = None,
) -> dict[str, Any]:

    if id not in shipments:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Invalid request,the given id is incorrect!"
        )

    shipment = shipments[id]

    # to update the values for specific fields
    #shipment.update(body)
    if content:
        shipment["content"] = content
    if weight:
        shipment["weight"] = weight
    if status:
        shipment["status"] = shipment_status

    #set the updated shipment data into the shipment we created
    shipments[id] = shipment
    return shipment



#DELETE METHOD - (deletes the existing data)
@app.delete("/shipment")
def delete_shipment(id:int)-> dict[str,Any]:
    if id not in shipments:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Invalid request, the given id doesn't exits!"
        )
    
    deleted_shipment = shipments.pop(id)
    return deleted_shipment # or you can just return {"detail" : f"the shipment with id#{id} is deleted!"}



# scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="scalar API")
