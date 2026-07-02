"""
Mock DB service — stores everything in st.session_state (in-memory only).
Data resets every time the Streamlit server restarts. Swap for a real
Firestore-backed version later if needed.
"""
import uuid
from datetime import date, timedelta

import pandas as pd
import streamlit as st

CATEGORIES = [
    "Salary", "Freelance", "Groceries", "Rent", "Utilities",
    "Transport", "Entertainment", "Dining Out", "Healthcare",
    "Shopping", "Travel", "Other",
]


def _store():
    if "mock_db" not in st.session_state:
        st.session_state.mock_db = {
            "transactions": _seed_transactions(),
            "investments": _seed_investments(),
            "goals": _seed_goals(),
            "preferences": {"currency": "INR", "darkMode": False, "widgetOrder": []},
        }
    return st.session_state.mock_db


def _seed_transactions():
    today = date.today()
    rows = [
        {"id": str(uuid.uuid4()), "type": "income", "category": "Salary",
         "description": "Monthly salary", "amount": 75000,
         "date": (today.replace(day=1)).isoformat()},
        {"id": str(uuid.uuid4()), "type": "expense", "category": "Rent",
         "description": "Apartment rent", "amount": 18000,
         "date": (today - timedelta(days=20)).isoformat()},
        {"id": str(uuid.uuid4()), "type": "expense", "category": "Groceries",
         "description": "Supermarket run", "amount": 3200,
         "date": (today - timedelta(days=12)).isoformat()},
        {"id": str(uuid.uuid4()), "type": "expense", "category": "Dining Out",
         "description": "Dinner with friends", "amount": 1500,
         "date": (today - timedelta(days=7)).isoformat()},
        {"id": str(uuid.uuid4()), "type": "expense", "category": "Transport",
         "description": "Fuel", "amount": 2200,
         "date": (today - timedelta(days=3)).isoformat()},
    ]
    return rows


def _seed_investments():
    return [
        {"id": str(uuid.uuid4()), "symbol": "AAPL", "quantity": 10,
         "purchasePrice": 150.0, "date": (date.today() - timedelta(days=200)).isoformat()},
        {"id": str(uuid.uuid4()), "symbol": "MSFT", "quantity": 5,
         "purchasePrice": 300.0, "date": (date.today() - timedelta(days=100)).isoformat()},
    ]


def _seed_goals():
    return [
        {"id": str(uuid.uuid4()), "title": "Emergency fund", "targetAmount": 100000,
         "currentAmount": 42000, "deadline": (date.today() + timedelta(days=180)).isoformat()},
    ]


# ---------------- Transactions ----------------
def get_transactions(uid: str) -> pd.DataFrame:
    rows = _store()["transactions"]
    if not rows:
        return pd.DataFrame(columns=["id", "type", "category", "description", "amount", "date"])
    df = pd.DataFrame(rows)
    return df.sort_values("date", ascending=False).reset_index(drop=True)


def add_transaction(uid, amount, category, tx_type, description, tx_date):
    _store()["transactions"].append({
        "id": str(uuid.uuid4()), "type": tx_type, "category": category,
        "description": description, "amount": amount, "date": tx_date,
    })


def update_transaction(uid, tx_id, **fields):
    for row in _store()["transactions"]:
        if row["id"] == tx_id:
            row.update(fields)


def delete_transaction(uid, tx_id):
    _store()["transactions"] = [r for r in _store()["transactions"] if r["id"] != tx_id]


# ---------------- Investments ----------------
def get_investments(uid: str) -> pd.DataFrame:
    rows = _store()["investments"]
    if not rows:
        return pd.DataFrame(columns=["id", "symbol", "quantity", "purchasePrice", "date"])
    return pd.DataFrame(rows)


def add_investment(uid, symbol, quantity, purchase_price, purchase_date):
    _store()["investments"].append({
        "id": str(uuid.uuid4()), "symbol": symbol.upper(), "quantity": quantity,
        "purchasePrice": purchase_price, "date": purchase_date,
    })


def delete_investment(uid, inv_id):
    _store()["investments"] = [r for r in _store()["investments"] if r["id"] != inv_id]


# ---------------- Goals ----------------
def get_goals(uid: str) -> pd.DataFrame:
    rows = _store()["goals"]
    if not rows:
        return pd.DataFrame(columns=["id", "title", "targetAmount", "currentAmount", "deadline"])
    return pd.DataFrame(rows)


def add_goal(uid, title, target, deadline):
    _store()["goals"].append({
        "id": str(uuid.uuid4()), "title": title, "targetAmount": target,
        "currentAmount": 0, "deadline": deadline,
    })


def update_goal_progress(uid, goal_id, new_amount):
    for row in _store()["goals"]:
        if row["id"] == goal_id:
            row["currentAmount"] = new_amount


def delete_goal(uid, goal_id):
    _store()["goals"] = [r for r in _store()["goals"] if r["id"] != goal_id]


# ---------------- Preferences ----------------
def get_preferences(uid: str) -> dict:
    return _store()["preferences"]


def update_preferences(uid, darkMode=False, currency="INR", widgetOrder=None):
    _store()["preferences"] = {
        "darkMode": darkMode, "currency": currency, "widgetOrder": widgetOrder or [],
    }
