from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    

class User(UserBase):
    pass


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
    user_email: str
    cost: int


class TransactionBase(BaseModel):
    title: str
    cost: float      
    trip_id: int 
    user_email: str 
    
    
class Transaction(TransactionBase):
    id: int
    
    class Config:
        orm_mode = True
        
class TripOut(Trip):
    users: list[User]


class TransactionCreate(TransactionBase):
    details: list[TransactionDetail]
    