from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from .database import Base


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    cost = Column(Integer)
    trip_id = Column(ForeignKey("trips.id"), nullable=False)

