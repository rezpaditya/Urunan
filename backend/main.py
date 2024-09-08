from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Trip(BaseModel):
    title: str
    text: Optional[str]


class Transaction(BaseModel):
    title: str
    cost: float


@app.get("/")
async def root():
    return {"message": "Hello World"}


# TRIPS
@app.get("/trips")
async def get_all_trips():
    return {"message": "I see all trips"}


@app.get("/trips/{id}")
async def get_trip(id):
    return {"message": f"I see trip with id: {id}"}


@app.post("/trips")
async def create_trip(trip: Trip):
    return trip


@app.patch("/trips")
async def create_trip(trip: Trip):
    return {"message": "Trip has been updated."}


@app.delete("/trips/{id}")
async def delete_trip(id):
    return {"message": f"Trip with id: {id} has been deleted."}

    
# TRANSACTION
@app.get("/transactions/{trip_id}")
async def get_all_transactions(trip_id):
    return {"message": f"I see all transaction of trip: {trip_id}"}


@app.get("/transactions/{trip_id}/{transaction_id}")
async def get_transaction(trip_id, transaction_id):
    return {"message": f"I see transaction with id: {transaction_id} and trip id: {trip_id}"}


@app.post("/transactions")
async def create_trip(transaction: Transaction):
    return transaction


@app.patch("/transactions")
async def create_trip(transaction: Transaction):
    return {"message": "Transaction has been updated."}


@app.delete("/transactions/{id}")
async def delete_transaction(id):
    return {"message": f"Transaction with id: {id} has been deleted."}
