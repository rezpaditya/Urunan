from pydantic import BaseModel
from typing import Optional


class Trip(BaseModel):
    id: int
    title: str
    text: Optional[str]


class Transaction(BaseModel):
    id: int
    title: str
    cost: float        