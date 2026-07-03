from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from ..db import schemas, models, crud
from ..dependency import get_db


router = APIRouter(
    prefix="/trips",
    tags=["trips"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[schemas.TripOut])
def get_all_trips(db: Session = Depends(get_db)):
    return crud.get(db, dao=models.Trip)


@router.get("/{id}", response_model=schemas.TripOut)
def get_trip(id, db: Session = Depends(get_db)):
    trip = crud.get_by_id(db, dao=models.Trip, id=id)
    if trip:
        return trip
    else:
        raise HTTPException(status_code=404, detail="failed to fetch trip...")


@router.post("/", response_model=schemas.TripOut)
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    trip_dao = models.Trip(title=trip.title, text=trip.text)
    for user in trip.users:
        user_dao = crud.get_by_id(db, models.User, user.id)
        trip_dao.users.append(user_dao)
    
    if db_trip := crud.create(db=db, dao=trip_dao):
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
    dao = models.Trip
    effected_row = db.scalars(select(dao).filter(dao.id == id)).first()
    effected_row.users = []
    db.add(effected_row)
    db.delete(effected_row)
    db.commit()
    return True


@router.get("/join/{trip_id}/{user_id}")
def join(trip_id, user_id, db: Session = Depends(get_db)):
    trip: models.Trip = crud.get_by_id(db, models.Trip, trip_id)
    user: models.User = crud.get_by_id(db, models.User, user_id)
    trip.users.append(user)
    db.commit()
    return trip


@router.post("/resolve")
def create_trip(resolved_debts: schemas.ResolvedDebts, db: Session = Depends(get_db)):
    db_resolved_debts = []
    for resolved_debt in resolved_debts.debts:
        db_resolved_debts.append(models.ResolvedDebt(
            trip_id=resolved_debt.trip_id,
            from_user=resolved_debt.from_user,
            to_user=resolved_debt.to_user,
            amount=resolved_debt.amount))
    db.bulk_save_objects(db_resolved_debts)
    db.commit()
    
    dao_trip = models.Trip
    db_data = db.query(dao_trip).filter(dao_trip.id == resolved_debts.trip_id)
    db_data.update({"is_resolved": True})
    db.commit()
    return resolved_debts
