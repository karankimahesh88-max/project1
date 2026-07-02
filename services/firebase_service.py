"""
Firebase bootstrap.

- Firebase Admin SDK -> Firestore (server-side, trusted) + ID token verification.
- Firebase Auth REST API -> email/password sign-up / sign-in (Admin SDK cannot
  verify a password itself, only the client REST API can, so we call it
  directly with `requests`).
"""
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

FIREBASE_AUTH_BASE = "https://identitytoolkit.googleapis.com/v1/accounts"


@st.cache_resource
def init_firebase_admin():
    """Initialize the Firebase Admin app exactly once per server process."""
    if not firebase_admin._apps:
        sa_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT_JSON"])
        cred = credentials.Certificate(sa_info)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def get_db():
    return init_firebase_admin()


def get_web_api_key() -> str:
    return st.secrets["FIREBASE_WEB_API_KEY"]
