from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.transaction import Transaction
from app.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == "income"
        )
        .scalar()
    )

    expense = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense"
        )
        .scalar()
    )

    transaction_count = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.user_id == user_id)
        .scalar()
    )

    balance = float(income) - float(expense)

    return {
        "total_income": float(income),
        "total_expense": float(expense),
        "balance": balance,
        "transaction_count": transaction_count
    }