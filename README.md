# AI Finance Assistant

AI Finance Assistant is a personal finance management web application that helps users track their income and expenses, automatically categorize expenses using Machine Learning, manage budgets, analyze spending, predict future spending, and get finance-related assistance through a chatbot.

## Features

- User Registration and Login
- JWT-based Authentication
- Add Income and Expense Transactions
- View, Update, and Delete Transactions
- Automatic Expense Categorization using Machine Learning
- Budget Management
- Financial Dashboard
- Income and Expense Visualization
- Spending Prediction
- AI-powered Financial Insights
- Finance Chatbot

## Machine Learning

### Expense Categorization

The application uses:

- TF-IDF Vectorization
- Logistic Regression

The model analyzes the transaction description and predicts a suitable category such as:

- Food
- Transport
- Entertainment
- Bills
- Health
- Education
- Shopping
- Income

### Spending Prediction

A Linear Regression model is used to provide a basic spending prediction based on monthly spending data.

## Technology Stack

### Frontend
- React.js
- Vite
- Axios
- Recharts

### Backend
- Python
- FastAPI
- Uvicorn

### Database
- MySQL
- SQLAlchemy
- PyMySQL

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib

### Authentication
- JWT
- bcrypt

## Project Structure

```text
ai-finance-assistant/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── main.py
│   │
│   ├── ml/
│   │   ├── train_model.py
│   │   ├── train_category_model.py
│   │   ├── spending_model.pkl
│   │   └── category_model.pkl
│   │
│   ├── .env
│   └── venv/
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── index.css
    │   └── main.jsx
    │
    ├── package.json
    └── vite.config.js