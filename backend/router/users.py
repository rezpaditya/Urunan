from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import schemas, models, crud
from ..dependency import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get(db, dao=models.User)
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="failed to fetch users...")
    

@router.post("/")
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    user_dao = models.User(email=user.email)
    return crud.create(db=db, dao=user_dao)
