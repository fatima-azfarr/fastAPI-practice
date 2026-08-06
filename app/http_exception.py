from typing import Any

from fastapi import FastAPI, HTTPException,status
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

@app.get("/shipment")
def get_shipment(id : int | None = None) -> dict[str,Any]:

    if id is None:
        id = max(shipments.keys())
        return shipments[id]

    # for when the id doesnt exit - we raise an httpexception
    if id not in shipments:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Given id doesn't exits!"

        )
    
    else:
        return shipments[id]

@app.get("/scalar",include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title = "scalar"
    )
