from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.dependencies import get_current_user
import joblib
import os

router = APIRouter(prefix="/category", tags=["AI Categorization"])

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "ml",
    "category_model.pkl"
)

model = joblib.load(MODEL_PATH)


class CategoryRequest(BaseModel):
    description: str


@router.post("/predict")
def predict_category(
    data: CategoryRequest,
    user_id: int = Depends(get_current_user)
):
    prediction = model.predict([data.description])[0]

    return {
        "description": data.description,
        "predicted_category": prediction
    }