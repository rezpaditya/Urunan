from sqlalchemy.orm import Session
from sqlalchemy.sql import select


def get_by_id(db: Session, dao, id: int):
    return db.query(dao).filter(dao.id == id).first()


def get(db: Session, dao, skip: int = 0, limit: int = 100):
    return db.query(dao).offset(skip).limit(limit).all()


def create(db: Session, dao):
    db.add(dao)
    db.commit()
    db.refresh(dao)
    return dao


def update(db: Session, dao, schema):
    db_data = db.query(dao).filter(dao.id == schema.id)
    db_data.update(schema.dict(exclude_unset=True))
    db.commit()
    return db_data.first()


def delete(db: Session, dao, id: int):
    effected_row = db.scalars(select(dao).filter(dao.id == id)).first()
    db.delete(effected_row)
    db.commit()
    return bool(effected_row)