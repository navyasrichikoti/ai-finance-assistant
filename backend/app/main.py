from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models import User, Transaction, Budget, Prediction, Insight
from app.routes.auth import router as auth_router
from app.routes.transactions import router as transaction_router
from app.routes.budgets import router as budget_router
from app.routes.dashboard import router as dashboard_router
from app.routes.prediction import router as prediction_router
from app.routes.category import router as category_router
from app.routes.insights import router as insights_router
from app.routes.chatbot import router as chatbot_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Finance Assistant API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
    "https://ai-finance-assistant-ten.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AI Finance Assistant API is running"
    }


app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(budget_router)
app.include_router(dashboard_router)
app.include_router(prediction_router)
app.include_router(category_router)
app.include_router(insights_router)
app.include_router(chatbot_router)