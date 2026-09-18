from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
import joblib
import os
import numpy as np

router = APIRouter(prefix="/prediction", tags=["Prediction"])

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "ml",
    "spending_model.pkl"
)

model = joblib.load(MODEL_PATH)


@router.get("/spending")
def predict_spending(
    month: int,
    user_id: int = Depends(get_current_user)
):
    prediction = model.predict(
        np.array([[month]])
    )[0]

    return {
        "month": month,
        "predicted_spending": round(float(prediction), 2)
    }