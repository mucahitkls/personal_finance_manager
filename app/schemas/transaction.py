from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    type: str
    amount: float
    description: str = None
    date: datetime


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int
