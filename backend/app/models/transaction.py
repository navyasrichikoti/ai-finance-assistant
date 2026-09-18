from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    date = Column(Date, nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)  # income / expense
    category = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)