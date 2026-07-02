"""Reusable Plotly chart builders (Streamlit's native chart-friendly library)."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def expense_pie_chart(category_df: pd.DataFrame):
    if category_df.empty:
        return None
    fig = px.pie(category_df, names="category", values="amount", hole=0.45,
                 title="Expenses by Category")
    fig.update_layout(margin=dict(t=50, b=10, l=10, r=10))
    return fig


def monthly_bar_chart(monthly_df: pd.DataFrame):
    if monthly_df.empty:
        return None
    fig = go.Figure()
    fig.add_bar(x=monthly_df["month"], y=monthly_df["income"], name="Income")
    fig.add_bar(x=monthly_df["month"], y=monthly_df["expense"], name="Expense")
    fig.update_layout(barmode="group", title="Monthly Income vs Expense",
                       margin=dict(t=50, b=10, l=10, r=10))
    return fig


def spending_trend_line(monthly_df: pd.DataFrame):
    if monthly_df.empty:
        return None
    fig = px.line(monthly_df, x="month", y="expense", markers=True,
                   title="Spending Trend Over Time")
    fig.update_layout(margin=dict(t=50, b=10, l=10, r=10))
    return fig


def portfolio_growth_chart(history_df: pd.DataFrame, symbol: str):
    if history_df.empty:
        return None
    fig = px.line(history_df, x="Date", y="Close", title=f"{symbol} Price History")
    fig.update_layout(margin=dict(t=50, b=10, l=10, r=10))
    return fig


def goal_progress_bar(current: float, target: float) -> float:
    """Returns a 0-1 fraction for use with st.progress()."""
    if target <= 0:
        return 0.0
    return max(0.0, min(1.0, current / target))
