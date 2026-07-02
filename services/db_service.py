"""
Firestore data-access layer.

Schema:
users/{uid}
    email, displayName, preferences: { darkMode, currency, widgetOrder }
users/{uid}/transactions/{txId}
    id, amount, category, type ("income" | "expense"), description, date (ISO str)
users/{uid}/investments/{invId}
    id, symbol, quantity, purchasePrice, purchaseDate (ISO str)
users/{uid}/goals/{goalId}
    id, title, targetAmount, currentAmount, deadline (ISO str), type
"""
import uuid
from datetime import datetime
import pandas as pd
from services.firebase_service import get_db

CATEGORIES = [
    "Food", "Bills", "Travel", "Shopping", "Entertainment",
    "Salary", "Investments", "Savings", "Other",
]


# ---------- Transactions ----------
def add_transaction(uid: str, amount: float, category: str, tx_type: str,
                     description: str, date: str) -> str:
    db = get_db()
    tx_id = str(uuid.uuid4())
    db.collection("users").document(uid).collection("transactions").document(tx_id).set({
        "id": tx_id,
        "amount": float(amount),
        "category": category,
        "type": tx_type,  # "income" or "expense"
        "description": description,
        "date": date,
    })
    return tx_id


def update_transaction(uid: str, tx_id: str, **fields) -> None:
    db = get_db()
    db.collection("users").document(uid).collection("transactions").document(tx_id).update(fields)


def delete_transaction(uid: str, tx_id: str) -> None:
    db = get_db()
    db.collection("users").document(uid).collection("transactions").document(tx_id).delete()


def get_transactions(uid: str) -> pd.DataFrame:
    db = get_db()
    docs = db.collection("users").document(uid).collection("transactions").stream()
    rows = [d.to_dict() for d in docs]
    if not rows:
        return pd.DataFrame(columns=["id", "amount", "category", "type", "description", "date"])
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date", ascending=False)


# ---------- Investments ----------
def add_investment(uid: str, symbol: str, quantity: float, purchase_price: float,
                    purchase_date: str) -> str:
    db = get_db()
    inv_id = str(uuid.uuid4())
    db.collection("users").document(uid).collection("investments").document(inv_id).set({
        "id": inv_id,
        "symbol": symbol.upper(),
        "quantity": float(quantity),
        "purchasePrice": float(purchase_price),
        "purchaseDate": purchase_date,
    })
    return inv_id


def delete_investment(uid: str, inv_id: str) -> None:
    db = get_db()
    db.collection("users").document(uid).collection("investments").document(inv_id).delete()


def get_investments(uid: str) -> pd.DataFrame:
    db = get_db()
    docs = db.collection("users").document(uid).collection("investments").stream()
    rows = [d.to_dict() for d in docs]
    if not rows:
        return pd.DataFrame(columns=["id", "symbol", "quantity", "purchasePrice", "purchaseDate"])
    return pd.DataFrame(rows)


# ---------- Goals ----------
def add_goal(uid: str, title: str, target_amount: float, deadline: str,
             goal_type: str = "savings", current_amount: float = 0.0) -> str:
    db = get_db()
    goal_id = str(uuid.uuid4())
    db.collection("users").document(uid).collection("goals").document(goal_id).set({
        "id": goal_id,
        "title": title,
        "targetAmount": float(target_amount),
        "currentAmount": float(current_amount),
        "deadline": deadline,
        "type": goal_type,
    })
    return goal_id


def update_goal_progress(uid: str, goal_id: str, current_amount: float) -> None:
    db = get_db()
    db.collection("users").document(uid).collection("goals").document(goal_id).update(
        {"currentAmount": float(current_amount)}
    )


def delete_goal(uid: str, goal_id: str) -> None:
    db = get_db()
    db.collection("users").document(uid).collection("goals").document(goal_id).delete()


def get_goals(uid: str) -> pd.DataFrame:
    db = get_db()
    docs = db.collection("users").document(uid).collection("goals").stream()
    rows = [d.to_dict() for d in docs]
    if not rows:
        return pd.DataFrame(columns=["id", "title", "targetAmount", "currentAmount", "deadline", "type"])
    return pd.DataFrame(rows)


# ---------- Preferences ----------
def get_preferences(uid: str) -> dict:
    db = get_db()
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        return doc.to_dict().get("preferences", {})
    return {}


def update_preferences(uid: str, **prefs) -> None:
    db = get_db()
    db.collection("users").document(uid).set({"preferences": prefs}, merge=True)
