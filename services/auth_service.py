"""
Mock auth service — NO real authentication.
Auto-signs in a fixed demo user so app.py's login screen is skipped entirely.
"""

DEMO_USER = {"uid": "demo-user-1", "email": "demo@localhost"}


def is_authenticated() -> bool:
    return True


def current_user() -> dict:
    return DEMO_USER


def sign_in(email: str, password: str) -> dict:
    return DEMO_USER


def sign_up(email: str, password: str, name: str) -> dict:
    return DEMO_USER


def start_session(data: dict) -> None:
    pass


def logout() -> None:
    pass
