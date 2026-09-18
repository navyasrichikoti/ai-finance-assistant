import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

texts = [
    "grocery shopping",
    "vegetables and fruits",
    "supermarket",
    "restaurant dinner",
    "pizza",
    "food delivery",
    "uber ride",
    "taxi fare",
    "bus ticket",
    "movie ticket",
    "netflix subscription",
    "electricity bill",
    "water bill",
    "internet bill",
    "mobile recharge",
    "doctor consultation",
    "medicine",
    "pharmacy",
    "college fees",
    "course fee",
    "books",
    "online shopping",
    "clothes purchase",
    "salary",
    "monthly salary"
]

categories = [
    "Food",
    "Food",
    "Food",
    "Food",
    "Food",
    "Food",
    "Transport",
    "Transport",
    "Transport",
    "Entertainment",
    "Entertainment",
    "Bills",
    "Bills",
    "Bills",
    "Bills",
    "Health",
    "Health",
    "Health",
    "Education",
    "Education",
    "Education",
    "Shopping",
    "Shopping",
    "Income",
    "Income"
]

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(texts, categories)

model_path = os.path.join(
    os.path.dirname(__file__),
    "category_model.pkl"
)

joblib.dump(model, model_path)

print("Expense category model trained successfully.")
print(f"Model saved at: {model_path}")