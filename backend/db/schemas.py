from pydantic import BaseModel
from typing import Optional


class TripBase(BaseModel):
    title: str
    text: Optional[str]


class TripCreate(TripBase):
    pass


class Trip(TripBase):
    id: int
    
    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    title: str
    cost: float      
    trip_id: int  
    

class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int   
    
    class Config:
        orm_mode = True
         