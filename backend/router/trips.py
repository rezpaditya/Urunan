from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import schemas, models, crud
from ..dependency import get_db


router = APIRouter(
    prefix="/trips",
    tags=["trips"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[schemas.TripOut])
def get_all_trips(db: Session = Depends(get_db)):
    trips = crud.get(db, dao=models.Trip)
    if trips:
        return trips
    else:
        raise HTTPException(status_code=404, detail="failed to fetch trips...")


@router.get("/{id}")
def get_trip(id, db: Session = Depends(get_db)):
    trip = crud.get_by_id(db, dao=models.Trip, id=id)
    if trip:
        return trip
    else:
        raise HTTPException(status_code=404, detail="failed to fetch trip...")


@router.post("/", response_model=schemas.TripOut)
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    # TODO: make the get_user dynamic
    user = crud.get_by_id(db, models.User, 1)
    dao = models.Trip(title=trip.title, text=trip.text, users=[user])
    db_trip = crud.create(db=db, dao=dao)
    if db_trip:
        return db_trip
    else:
        raise HTTPException(status_code=401, detail="Failed to create trip...")


@router.patch("/", response_model=schemas.Trip)
def update_trip(trip: schemas.Trip, db: Session = Depends(get_db)):
    db_trip = crud.update(db=db, dao=models.Trip, schema=trip)
    if db_trip:
        return db_trip
    else:
        raise HTTPException(status_code=401, detail=f"Failed to update article with ID {trip.id}...")


@router.delete("/{id}")
def delete_trip(id, db: Session = Depends(get_db)):
    return crud.delete(db=db, dao=models.Trip, id=id)


@router.get("/join/{trip_id}/{user_id}")
def join(trip_id, user_id, db: Session = Depends(get_db)):
    trip: models.Trip = crud.get_by_id(db, models.Trip, trip_id)
    user: models.User = crud.get_by_id(db, models.User, user_id)
    trip.users.append(user)
    db.commit()
    return trip
