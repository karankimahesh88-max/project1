"""Plotly chart builders used by the Streamlit pages."""
import plotly.express as px
import plotly.graph_objects as go


def expense_pie_chart(df):
    if df is None or df.empty:
        return None
    fig = px.pie(df, names="category", values="amount", hole=0.4)
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    return fig


def monthly_bar_chart(df):
    if df is None or df.empty:
        return None
    fig = px.bar(df, x="month", y="amount", color="type", barmode="group")
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    return fig


def spending_trend_line(df):
    if df is None or df.empty:
        return None
    expense_df = df[df["type"] == "expense"]
    if expense_df.empty:
        return None
    fig = px.line(expense_df, x="month", y="amount", markers=True)
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    return fig


def portfolio_growth_chart(hist_df, symbol: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_df["date"], y=hist_df["close"], mode="lines", name=symbol))
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), yaxis_title="Price")
    return fig


def goal_progress_bar(current, target) -> float:
    if not target:
        return 0.0
    return max(0.0, min(1.0, current / target))
