from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.models.prediction import Prediction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.dependencies import get_current_user
import joblib
import os

router = APIRouter(prefix="/transactions", tags=["Transactions"])

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "ml",
    "category_model.pkl"
)

category_model = joblib.load(MODEL_PATH)


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    category = data.category

    if data.type == "expense" and not category:
        category = category_model.predict([data.description])[0]

    transaction = Transaction(
        user_id=user_id,
        date=data.date,
        description=data.description,
        amount=data.amount,
        type=data.type,
        category=category
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    if data.type == "expense" and category:
        prediction = Prediction(
            transaction_id=transaction.id,
            predicted_category=category
        )
        db.add(prediction)
        db.commit()

    return transaction


@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.date.desc())
        .all()
    )


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    category = data.category

    if data.type == "expense" and not category:
        category = category_model.predict([data.description])[0]

    transaction.date = data.date
    transaction.description = data.description
    transaction.amount = data.amount
    transaction.type = data.type
    transaction.category = category

    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.query(Prediction).filter(
        Prediction.transaction_id == transaction_id
    ).delete()

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction deleted successfully"
    }