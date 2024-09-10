from fastapi import FastAPI
from .db import models
from .db.database import engine
from .router import trips, transactions


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(trips.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

    