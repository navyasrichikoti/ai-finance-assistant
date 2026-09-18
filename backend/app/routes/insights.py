from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.transaction import Transaction
from app.models.insight import Insight
from app.dependencies import get_current_user

router = APIRouter(prefix="/insights", tags=["AI Insights"])


@router.get("/")
def get_insights(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    expense_total = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense"
        )
        .scalar()
    )

    income_total = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == "income"
        )
        .scalar()
    )

    top_category = (
        db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("total")
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.category.isnot(None)
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .first()
    )

    insights = []

    if income_total > 0 and expense_total > income_total:
        insights.append("Your expenses are higher than your income.")

    if top_category:
        insights.append(
            f"Your highest spending category is {top_category.category}."
        )

    if not insights:
        insights.append("Your spending is currently within your recorded income.")

    return {
        "total_income": float(income_total),
        "total_expense": float(expense_total),
        "insights": insights
    }