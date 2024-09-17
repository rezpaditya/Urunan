from fastapi import FastAPI
from sqlalchemy import event
from fastapi.middleware.cors import CORSMiddleware
from .db import models, database
from .db.database import engine
from .router import trips, transactions


# seeder
event.listen(models.User.__table__, 'after_create', database.initialize_table)

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
