from typing import Any

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


# order of the requests matter when we have positional parameters
@app.get("/shipment/latest")
def get_latest_shipment():
    return{
        "id" : 264789,
        "Content" : "glassware",
        "weight" : 20,
        "status" : "placed"
    }

# created route handler that receives a path parameter
@app.get("/shipment/{id}")
def get_shipment(id : int) -> dict[str,Any]:
    return{
        "id" : id,
        "Content" : "wooden box",
        "weight" : 100,
        "status" : "in transit"
    }

@app.get("/scalar", include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title = "scalar API"
    )