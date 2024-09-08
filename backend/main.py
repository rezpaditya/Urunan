from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/trips")
async def get_all_trips():
    return {"message": "I see all trips"}


@app.get("/trips/{id}")
async def get_trip(id):
    return {"message": f"I see trip with id: {id}"}


@app.get("/transactions/{trip_id}")
async def get_all_transactions(trip_id):
    return {"message": f"I see all transaction of trip: {trip_id}"}


@app.get("/transactions/{trip_id}/{transaction_id}")
async def get_transaction(trip_id, transaction_id):
    return {"message": f"I see transaction with id: {transaction_id} and trip id: {trip_id}"}
