from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.transaction import Transaction
from app.dependencies import get_current_user

router = APIRouter(prefix="/chatbot", tags=["Finance Chatbot"])


class ChatRequest(BaseModel):
    message: str


@router.post("/ask")
def ask_chatbot(
    data: ChatRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    message = data.message.lower()

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

    balance = float(income) - float(expense)

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

    if "expense" in message or "spending" in message:
        reply = f"Your total recorded expenses are ₹{float(expense):.2f}."

    elif "income" in message:
        reply = f"Your total recorded income is ₹{float(income):.2f}."

    elif "balance" in message or "money" in message:
        reply = f"Your current balance is ₹{balance:.2f}."

    elif "category" in message or "spend most" in message:
        if top_category:
            reply = (
                f"Your highest spending category is "
                f"{top_category.category}, with ₹{float(top_category.total):.2f}."
            )
        else:
            reply = "You do not have enough categorized expenses yet."

    elif "save" in message or "saving" in message:
        reply = (
            "Try setting a monthly budget for your highest spending "
            "category and review your expenses regularly."
        )

    else:
        reply = (
            "I can help you with your income, expenses, balance, "
            "spending categories, and saving tips."
        )

    return {
        "question": data.message,
        "answer": reply
    }