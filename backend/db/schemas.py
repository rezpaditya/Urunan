from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: str
    

class User(UserBase):
    id: int


class TripBase(BaseModel):
    title: str
    text: Optional[str]
    users: list[User]


class TripCreate(TripBase):
    pass


class Trip(TripBase):
    id: int
    
    class Config:
        orm_mode = True


class TransactionDetail(BaseModel):
    email: str
    cost: float


class TransactionBase(BaseModel):
    title: str
    cost: float      
    trip_id: int 
    email: str 
    
    
class Transaction(TransactionBase):
    id: int
    
    class Config:
        orm_mode = True
        

class TransactionCreate(TransactionBase):
    details: list[TransactionDetail]
    
    
class TransactionOut(TransactionBase):
    id: int
    transaction_date: datetime
    receipt: Optional[str]
    details: list[TransactionDetail]


class TransactionEdit(BaseModel):
    id: int
    title: Optional[str] = None
    transaction_date: Optional[datetime] = None
    receipt: Optional[str] = None
    

class TripOut(Trip):
    is_resolved: bool
    users: list[User]
    transactions: list[TransactionOut]


class ResolvedDebt(BaseModel):
    trip_id: int
    from_user: int
    to_user: int
    amount: int

class ResolvedDebts(BaseModel):
    trip_id: int
    debts: list[ResolvedDebt]
    