import os
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression


# Sample monthly spending data for initial model
months = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(-1, 1)
spending = np.array([12000, 13500, 12800, 14500, 15000, 15800, 16200, 17000])

model = LinearRegression()
model.fit(months, spending)

model_path = os.path.join(
    os.path.dirname(__file__),
    "spending_model.pkl"
)

joblib.dump(model, model_path)

print("Spending prediction model trained successfully.")
print(f"Model saved at: {model_path}")