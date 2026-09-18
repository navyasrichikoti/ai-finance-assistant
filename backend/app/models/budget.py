from sqlalchemy import Column, Integer, Float, String, ForeignKey

from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    month = Column(String(7), nullable=False)  # YYYY-MM
    category = Column(String(50), nullable=True)
    limit_amount = Column(Float, nullable=False)