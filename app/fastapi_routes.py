from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import Session

from app.database.session import create_db_table

from .database.sql_database import Database
from .schema import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatusUpdate,
    ShipmentUpdate,
)


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    create_db_table()
    yield

app = FastAPI(lifespan=lifespan_handler)

db = Database()


# GET METHOD
@app.get("/shipment/{id}", response_model=ShipmentRead)
def get_shipment(id: int,session:Session = Depends) -> ShipmentRead:
    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, given id doesn't exist!",
        )

    return ShipmentRead(**shipment)


# POST METHOD
@app.post("/shipment", response_model=ShipmentRead)
def submit_shipments(shipment: ShipmentCreate) -> ShipmentRead:
    new_id = db.create(shipment)
    return db.get(new_id)


# PUT METHOD
@app.put("/shipment/{id}", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate) -> ShipmentRead:
    updated = db.update(id, shipment)

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, given id doesn't exist!"
        )

    return updated


# PATCH METHOD
@app.patch("/shipment/{id}", response_model=ShipmentRead)
def patch_shipment(id: int, shipment: ShipmentStatusUpdate) -> ShipmentRead:
    updated = db.patch(id, shipment)

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid request, given id doesn't exist!"
        )

    return updated


# DELETE METHOD
@app.delete("/shipment/{id}")
def delete_shipment(id: int) -> dict[str, Any]:
    db.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted."}


# Scalar documentation
@app.get("/scalar", include_in_schema=False)
def scalar_documentation():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )