from typing import Any

from fastapi import FastAPI
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


# to get the latest shipment
@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]

# to get shipments thru id
@app.get("/shipment/{id}")
def get_shipment(id : int) -> dict[str,Any]:
    if id not in shipments:
        return {"details": "The given ID doesnt exits!"}
    else:
        return shipments[id]


@app.get("/scalar", include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title = "scalar API"
    )