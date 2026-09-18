from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetResponse)
def create_budget(
    data: BudgetCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    budget = Budget(
        user_id=user_id,
        month=data.month,
        category=data.category,
        limit_amount=data.limit_amount
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return budget


@router.get("/", response_model=list[BudgetResponse])
def get_budgets(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .order_by(Budget.month.desc())
        .all()
    )