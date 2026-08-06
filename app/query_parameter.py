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

# QUERY PARAMETERS
# they are parameters which can be given to our routes in the url
# ? - question mark to indicate we are going to use query parameters and then the parameter itself (? name=value)
# if we provide any query parameters to our route endpoint, that is the URL, it will get passed on to our function.

@app.get("/shipment")
def get_shipment(id : int | None = None) -> dict[str,Any]:
    

    if id is None:
        id = max(shipments.keys())
        return shipments[id]
    
    if id not in shipments:
        return {"details" : "Invalid ID, it doesnt exits!"}
    
    else:
        return shipments[id]


@app.get("/scalar", include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title = "scalar API"
    )