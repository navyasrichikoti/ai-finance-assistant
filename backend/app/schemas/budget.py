from pydantic import BaseModel


class BudgetCreate(BaseModel):
    month: str
    category: str | None = None
    limit_amount: float


class BudgetResponse(BudgetCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True