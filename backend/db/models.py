from sqlalchemy import Column, String, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from .database import Base


trip_user_association = Table(
    'trip_user',
    Base.metadata,
    Column('trip_id', Integer, ForeignKey('trips.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

transaction_user_association = Table(
    'transaction_user',
    Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('cost', Integer)
)

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    users = relationship("User", secondary=trip_user_association, back_populates="trips")
    transactions = relationship("Transaction")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    cost = Column(Integer)
    trip_id = Column(ForeignKey("trips.id"), nullable=False)
    user_email = Column(String)
    users = relationship("User", secondary=transaction_user_association)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    trips = relationship("Trip", secondary=trip_user_association, back_populates="users")
    