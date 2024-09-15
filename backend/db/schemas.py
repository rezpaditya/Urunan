from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    

class User(UserBase):
    pass


class TripBase(BaseModel):
    title: str
    text: Optional[str]
    users: Optional[User]


class TripCreate(TripBase):
    pass


class Trip(TripBase):
    id: int
    
    class Config:
        orm_mode = True
        
class TripOut(Trip):
    users: list[User]


class TransactionBase(BaseModel):
    title: str
    cost: float      
    trip_id: int 
    user_email: str 
    

class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int   
    
    class Config:
        orm_mode = True
         
         
