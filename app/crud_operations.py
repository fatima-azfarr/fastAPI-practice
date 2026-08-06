from typing import Any

from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
     12345 : {
        "content" : "wooden box",
        "weight" : 20,
        "status" : "in transit"
    },

     12346 : {
        "content" : "glassware",
        "weight" : 10,
        "status" : "placed"
    },
     12347 : {
            "content" : "mobile phones",
            "weight" : 50,
            "status" : "placed"
    },
     12348 : {
            "content" : "keyboard",
            "weight" : 10,
            "status" : "cancelled"
        }
}

# GET METHOD
@app.get("/shipment")
def get_shipment(id : int | None = None) -> dict[str,Any]:

    if id is None:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Invalid request, given id doesn't exits!"
        )
    
    else:
        return shipments[id]
    

# POST METHOD
# to get data from the client to the server

@app.post("/shipment")
def submit_shipment(content: str,weight: float) -> dict[str,int]:

    if weight > 25 :
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Invalid Request, the weight exceeds the given limit (i.e 25 kgs)"
        )
    
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content" : content,
        "weight" : weight
    }
    return {"id": new_id}
    


@app.get("/scalar",include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "scalar API"
    )

