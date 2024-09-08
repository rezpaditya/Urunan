from fastapi import APIRouter
from backend.db import schemas


router = APIRouter(
    prefix="/trips",
    tags=["trips"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_all_trips():
    return {"message": "I see all trips"}


@router.get("/{id}")
async def get_trip(id):
    return {"message": f"I see trip with id: {id}"}


@router.post("/")
async def create_trip(trip: schemas.Trip):
    return trip


@router.patch("/")
async def create_trip(trip: schemas.Trip):
    return {"message": "schemas.Trip has been updated."}


@router.delete("/{id}")
async def delete_trip(id):
    return {"message": f"schemas.Trip with id: {id} has been deleted."}
