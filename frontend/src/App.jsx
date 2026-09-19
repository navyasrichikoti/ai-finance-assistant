import { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const API = "https://ai-finance-assistant-b6em.onrender.com";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isRegister, setIsRegister] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [summary, setSummary] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [insights, setInsights] = useState([]);
  const [budgets, setBudgets] = useState([]);

  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [type, setType] = useState("expense");

  const [budgetCategory, setBudgetCategory] = useState("");
  const [budgetLimit, setBudgetLimit] = useState("");

  const [prediction, setPrediction] = useState(null);

  const [chatMessage, setChatMessage] = useState("");
  const [chatReply, setChatReply] = useState("");

  const [editingTransaction, setEditingTransaction] = useState(null);

  const authHeaders = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const loadDashboard = async () => {
    try {
      const summaryRes = await axios.get(
        `${API}/dashboard/summary`,
        authHeaders
      );

      const transactionsRes = await axios.get(
        `${API}/transactions/`,
        authHeaders
      );

      const insightsRes = await axios.get(
        `${API}/insights/`,
        authHeaders
      );

      const budgetsRes = await axios.get(
        `${API}/budgets/`,
        authHeaders
      );

      setSummary(summaryRes.data);
      setTransactions(transactionsRes.data);
      setInsights(insightsRes.data.insights);
      setBudgets(budgetsRes.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    if (token) {
      loadDashboard();
    }
  }, [token]);

  const handleAuth = async (e) => {
    e.preventDefault();

    try {
      if (isRegister) {
        const response = await axios.post(`${API}/auth/register`, {
          name,
          email,
          password,
        });

        localStorage.setItem("token", response.data.access_token);
        setToken(response.data.access_token);
      } else {
        const response = await axios.post(`${API}/auth/login`, {
          email,
          password,
        });

        localStorage.setItem("token", response.data.access_token);
        setToken(response.data.access_token);
      }
    } catch (error) {
      alert(error.response?.data?.detail || "Authentication failed");
    }
  };

  const addTransaction = async (e) => {
    e.preventDefault();

    try {
      await axios.post(
        `${API}/transactions/`,
        {
          date: new Date().toISOString().split("T")[0],
          description,
          amount: Number(amount),
          type,
        },
        authHeaders
      );

      setDescription("");
      setAmount("");

      await loadDashboard();

      alert("Transaction added successfully!");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Failed to add transaction"
      );
    }
  };

  const updateTransaction = async (e) => {
    e.preventDefault();

    try {
      await axios.put(
        `${API}/transactions/${editingTransaction.id}`,
        {
          date: editingTransaction.date,
          description: editingTransaction.description,
          amount: Number(editingTransaction.amount),
          type: editingTransaction.type,
          category: editingTransaction.category || null,
        },
        authHeaders
      );

      setEditingTransaction(null);

      await loadDashboard();

      alert("Transaction updated successfully!");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Failed to update transaction"
      );
    }
  };

  const deleteTransaction = async (id) => {
    if (!window.confirm("Delete this transaction?")) {
      return;
    }

    try {
      await axios.delete(
        `${API}/transactions/${id}`,
        authHeaders
      );

      await loadDashboard();

      alert("Transaction deleted successfully!");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Failed to delete transaction"
      );
    }
  };

  const addBudget = async (e) => {
    e.preventDefault();

    try {
      await axios.post(
        `${API}/budgets/`,
        {
          month: new Date().toISOString().slice(0, 7),
          category: budgetCategory || null,
          limit_amount: Number(budgetLimit),
        },
        authHeaders
      );

      setBudgetCategory("");
      setBudgetLimit("");

      await loadDashboard();

      alert("Budget created successfully!");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Failed to create budget"
      );
    }
  };

  const getPrediction = async () => {
    try {
      const currentMonth = new Date().getMonth() + 1;

      const response = await axios.get(
        `${API}/prediction/spending?month=${currentMonth}`,
        authHeaders
      );

      setPrediction(response.data);
    } catch (error) {
      alert("Prediction failed");
    }
  };

  const askChatbot = async (e) => {
    e.preventDefault();

    if (!chatMessage.trim()) {
      return;
    }

    try {
      const response = await axios.post(
        `${API}/chatbot/ask`,
        {
          message: chatMessage,
        },
        authHeaders
      );

      setChatReply(response.data.answer);
      setChatMessage("");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Chatbot request failed"
      );
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setSummary(null);
  };

  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <h1>AI Finance Assistant</h1>

          <p>Smart personal finance management</p>

          <form onSubmit={handleAuth}>
            {isRegister && (
              <input
                type="text"
                placeholder="Full Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            )}

            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <button type="submit">
              {isRegister ? "Create Account" : "Login"}
            </button>
          </form>

          <p
            className="switch"
            onClick={() => setIsRegister(!isRegister)}
          >
            {isRegister
              ? "Already have an account? Login"
              : "New user? Create an account"}
          </p>
        </div>
      </div>
    );
  }

  const chartData = [
    {
      name: "Income",
      value: summary?.total_income || 0,
    },
    {
      name: "Expenses",
      value: summary?.total_expense || 0,
    },
  ];

  return (
    <div className="dashboard">
      <header>
        <div>
          <h1>AI Finance Assistant</h1>
          <p>Personal Finance Dashboard</p>
        </div>

        <button onClick={logout}>Logout</button>
      </header>

      <main>
        <section className="cards">
          <div className="card">
            <h3>Total Income</h3>
            <h2>
              ₹{summary?.total_income?.toFixed(2) || "0.00"}
            </h2>
          </div>

          <div className="card">
            <h3>Total Expenses</h3>
            <h2>
              ₹{summary?.total_expense?.toFixed(2) || "0.00"}
            </h2>
          </div>

          <div className="card">
            <h3>Balance</h3>
            <h2>
              ₹{summary?.balance?.toFixed(2) || "0.00"}
            </h2>
          </div>

          <div className="card">
            <h3>Transactions</h3>
            <h2>{summary?.transaction_count || 0}</h2>
          </div>
        </section>

        <section className="panel">
          <h2>Expense Overview</h2>

          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} />
                  ))}
                </Pie>

                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="content-grid">
          <div className="panel">
            <h2>Add Transaction</h2>

            <form onSubmit={addTransaction}>
              <input
                type="text"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />

              <input
                type="number"
                placeholder="Amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />

              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>

              <button type="submit">
                Add Transaction
              </button>
            </form>

            <p className="ai-note">
              ✨ Expense category will be predicted automatically by AI.
            </p>
          </div>

          <div className="panel">
            <h2>AI Insights</h2>

            {insights.length > 0 ? (
              insights.map((insight, index) => (
                <div className="insight" key={index}>
                  💡 {insight}
                </div>
              ))
            ) : (
              <p>No insights available yet.</p>
            )}
          </div>
        </section>

        <section className="panel">
          <h2>Budget Management</h2>

          <form onSubmit={addBudget}>
            <input
              type="text"
              placeholder="Category (e.g. Food)"
              value={budgetCategory}
              onChange={(e) => setBudgetCategory(e.target.value)}
            />

            <input
              type="number"
              placeholder="Budget Limit"
              value={budgetLimit}
              onChange={(e) => setBudgetLimit(e.target.value)}
              required
            />

            <button type="submit">
              Create Budget
            </button>
          </form>

          <h3>Current Budgets</h3>

          {budgets.length === 0 ? (
            <p>No budgets created yet.</p>
          ) : (
            budgets.map((budget) => (
              <div className="insight" key={budget.id}>
                <strong>
                  {budget.category || "Overall"}
                </strong>

                <br />

                Month: {budget.month}

                <br />

                Limit: ₹{budget.limit_amount}
              </div>
            ))
          )}
        </section>

        <section className="panel">
          <h2>Spending Prediction</h2>

          <button onClick={getPrediction}>
            Predict This Month's Spending
          </button>

          {prediction && (
            <div className="prediction">
              <h3>Predicted Spending</h3>

              <h2>
                ₹{prediction.predicted_spending}
              </h2>

              <p>
                Month: {prediction.month}
              </p>
            </div>
          )}
        </section>

        <section className="panel">
          <h2>🤖 Finance Chatbot</h2>

          <p>
            Ask questions about your income, expenses,
            balance, spending categories, or saving.
          </p>

          <form onSubmit={askChatbot}>
            <input
              type="text"
              placeholder="Ask something like: What are my expenses?"
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              required
            />

            <button type="submit">
              Ask AI
            </button>
          </form>

          {chatReply && (
            <div className="insight">
              <strong>AI:</strong> {chatReply}
            </div>
          )}
        </section>

        {editingTransaction && (
          <section className="panel">
            <h2>Edit Transaction</h2>

            <form onSubmit={updateTransaction}>
              <input
                type="date"
                value={editingTransaction.date}
                onChange={(e) =>
                  setEditingTransaction({
                    ...editingTransaction,
                    date: e.target.value,
                  })
                }
                required
              />

              <input
                type="text"
                value={editingTransaction.description}
                onChange={(e) =>
                  setEditingTransaction({
                    ...editingTransaction,
                    description: e.target.value,
                  })
                }
                required
              />

              <input
                type="number"
                value={editingTransaction.amount}
                onChange={(e) =>
                  setEditingTransaction({
                    ...editingTransaction,
                    amount: e.target.value,
                  })
                }
                required
              />

              <select
                value={editingTransaction.type}
                onChange={(e) =>
                  setEditingTransaction({
                    ...editingTransaction,
                    type: e.target.value,
                  })
                }
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>

              <button type="submit">
                Update Transaction
              </button>

              <button
                type="button"
                onClick={() => setEditingTransaction(null)}
                style={{ marginLeft: "8px" }}
              >
                Cancel
              </button>
            </form>
          </section>
        )}

        <section className="panel">
          <h2>Recent Transactions</h2>

          {transactions.length === 0 ? (
            <p>No transactions yet.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Type</th>
                  <th>Category</th>
                  <th>Amount</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {transactions.map((transaction) => (
                  <tr key={transaction.id}>
                    <td>{transaction.date}</td>

                    <td>{transaction.description}</td>

                    <td>{transaction.type}</td>

                    <td>
                      {transaction.category || "-"}
                    </td>

                    <td>
                      ₹{transaction.amount}
                    </td>

                    <td>
                      <button
                        onClick={() =>
                          setEditingTransaction(transaction)
                        }
                      >
                        Edit
                      </button>

                      <button
                        onClick={() =>
                          deleteTransaction(transaction.id)
                        }
                        style={{ marginLeft: "8px" }}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;