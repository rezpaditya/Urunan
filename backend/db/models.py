from sqlalchemy import Column, String, Integer, ForeignKey, String, Table, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


trip_user_association = Table(
    'trip_user',
    Base.metadata,
    Column('trip_id', Integer, ForeignKey('trips.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class TransactionDetail(Base):
    __tablename__ = "transaction_detail"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    transaction = relationship("Transaction", back_populates="details")
    email = Column(String)
    cost = Column(Float)
    

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    is_resolved = Column(Boolean, default=False)
    users = relationship("User", secondary=trip_user_association, back_populates="trips")
    transactions = relationship("Transaction", cascade="all, delete")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    cost = Column(Float)
    trip_id = Column(ForeignKey("trips.id"), nullable=False)
    email = Column(String)
    receipt = Column(String)
    transaction_date = Column(DateTime, default=datetime.now(), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    details = relationship("TransactionDetail", back_populates="transaction", cascade="all, delete")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    trips = relationship("Trip", secondary=trip_user_association, back_populates="users")


class ResolvedDebt(Base):
    __tablename__ = "resolved_debt"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(ForeignKey("trips.id"), nullable=False)
    from_user = Column(ForeignKey("users.id"), nullable=False)
    to_user = Column(ForeignKey("users.id"), nullable=False)
    amount = Column(Integer)
    