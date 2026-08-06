from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

# create fastapi instance - to mark the function as API endpoint handler or route handler
# for that we use the decorator

app = FastAPI()

#--------------------------------------
#----API ENDPOINT HANDLER FORMATION----
#--------------------------------------

# using get method to get the data
# inside the parenthesis we need to provide route or path for the route handler
# path can be nested like "/seller/shipment"

@app.get("/shipment")
def get_shipment_data():
    return{
        "id" : 63729,
        "Content" : "Mobile Phone",
        "Status" : "in transit",
        "Quantity" : 100
    }

# defined custom documentation using open API specificaton

@app.get("/scalar",include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "scalar API"
    )

