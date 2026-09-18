from pydantic import BaseModel
from datetime import date


class TransactionCreate(BaseModel):
    date: date
    description: str
    amount: float
    type: str
    category: str | None = None


class TransactionResponse(TransactionCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True