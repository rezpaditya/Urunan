from fastapi import FastAPI
from sqlalchemy import event
from fastapi.middleware.cors import CORSMiddleware
from .db import models, database
from .db.database import engine
from .router import trips, transactions, users


# seeder
event.listen(models.User.__table__, 'after_create', database.initialize_table)

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# TODO: define allow origin
# origins = [
#     "*",
#     "http://127.0.0.1:8080",
#     "http://178.128.143.5:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router)
app.include_router(transactions.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
