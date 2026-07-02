"""
Authentication service.

Uses the Firebase Auth REST API for sign-up / sign-in (this is the same
endpoint the JS SDK calls under the hood), then stores the resulting
uid / idToken / email in st.session_state to act as our "session".
"""
import requests
import streamlit as st
from services.firebase_service import get_web_api_key, get_db

AUTH_BASE = "https://identitytoolkit.googleapis.com/v1/accounts"


def _default_preferences() -> dict:
    return {
        "darkMode": False,
        "currency": "INR",
        "widgetOrder": ["summary", "expensePie", "monthlyBar", "trendLine", "portfolio"],
    }


def sign_up(email: str, password: str, display_name: str = "") -> dict:
    """Create a new Firebase Auth user, then seed their Firestore profile."""
    url = f"{AUTH_BASE}:signUp?key={get_web_api_key()}"
    resp = requests.post(
        url,
        json={"email": email, "password": password, "returnSecureToken": True},
        timeout=10,
    )
    data = resp.json()
    if resp.status_code != 200:
        raise ValueError(data.get("error", {}).get("message", "Sign up failed"))

    uid = data["localId"]
    db = get_db()
    db.collection("users").document(uid).set(
        {
            "email": email,
            "displayName": display_name or email.split("@")[0],
            "preferences": _default_preferences(),
        }
    )
    return data


def sign_in(email: str, password: str) -> dict:
    """Sign in an existing user with email/password."""
    url = f"{AUTH_BASE}:signInWithPassword?key={get_web_api_key()}"
    resp = requests.post(
        url,
        json={"email": email, "password": password, "returnSecureToken": True},
        timeout=10,
    )
    data = resp.json()
    if resp.status_code != 200:
        raise ValueError(data.get("error", {}).get("message", "Sign in failed"))
    return data


def start_session(auth_data: dict) -> None:
    """Persist the logged-in user in Streamlit's session state."""
    st.session_state["user"] = {
        "uid": auth_data["localId"],
        "email": auth_data["email"],
        "id_token": auth_data["idToken"],
        "refresh_token": auth_data.get("refreshToken"),
    }


def logout() -> None:
    for key in ("user",):
        st.session_state.pop(key, None)


def current_user() -> dict | None:
    return st.session_state.get("user")


def is_authenticated() -> bool:
    return "user" in st.session_state


def require_login() -> dict:
    """Call at the top of any protected page. Stops execution if not logged in."""
    user = current_user()
    if not user:
        st.warning("Please log in to view this page.")
        st.stop()
    return user
