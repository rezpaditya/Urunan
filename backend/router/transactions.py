from fastapi import APIRouter
from backend.db import schemas


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{trip_id}")
async def get_all_transactions(trip_id):
    return {"message": f"I see all transaction of trip: {trip_id}"}


@router.get("/{trip_id}/{transaction_id}")
async def get_transaction(trip_id, transaction_id):
    return {"message": f"I see transaction with id: {transaction_id} and trip id: {trip_id}"}


@router.post("/")
async def create_trip(transaction: schemas.Transaction):
    return transaction


@router.patch("/")
async def create_trip(transaction: schemas.Transaction):
    return {"message": "schemas.Transaction has been updated."}


@router.delete("/{id}")
async def delete_transaction(id):
    return {"message": f"schemas.Transaction with id: {id} has been deleted."}
