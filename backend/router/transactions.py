from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import schemas, models, crud
from ..dependency import get_db


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Transaction])
def get_all_transactions(db: Session = Depends(get_db)):
    return crud.get(db, dao=models.Transaction)
    # TODO: handle exception


@router.get("/{id}", response_model=schemas.TransactionCreate)
def get_transaction(id, db: Session = Depends(get_db)):
    return crud.get_by_id(db, dao=models.Transaction, id=id)


@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    details = []
    for detail in transaction.details:
        details.append(models.TransactionDetail(email=detail.email, cost=detail.cost))
    dao = models.Transaction(title=transaction.title, cost=transaction.cost, trip_id=transaction.trip_id, email=transaction.email, details=details)
    return crud.create(db=db, dao=dao)

@router.patch("/")
def update_transaction(transaction: schemas.Transaction, db: Session = Depends(get_db)):
    return crud.update(db=db, dao=models.Transaction, schema=transaction)


@router.delete("/{id}")
def delete_transaction(id, db: Session = Depends(get_db)):
    return crud.delete(db=db, dao=models.Transaction, id=id)
