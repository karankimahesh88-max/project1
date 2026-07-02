"""
Pure functions that turn raw transactions / investments into insights.
Kept dependency-free from Streamlit so they're easy to unit test.
"""
import pandas as pd


def monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Return income/expense totals grouped by month (YYYY-MM)."""
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expense"])
    d = df.copy()
    d["month"] = d["date"].dt.to_period("M").astype(str)
    grouped = d.pivot_table(index="month", columns="type", values="amount", aggfunc="sum", fill_value=0)
    for col in ("income", "expense"):
        if col not in grouped:
            grouped[col] = 0
    return grouped.reset_index().sort_values("month")


def category_breakdown(df: pd.DataFrame, tx_type: str = "expense") -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    d = df[df["type"] == tx_type]
    return d.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False)


def savings_ratio(df: pd.DataFrame) -> float:
    """(income - expense) / income, as a percentage."""
    income = df.loc[df["type"] == "income", "amount"].sum()
    expense = df.loc[df["type"] == "expense", "amount"].sum()
    if income == 0:
        return 0.0
    return round(((income - expense) / income) * 100, 2)


def month_over_month_change(df: pd.DataFrame, category: str | None = None) -> float | None:
    """% change in spending between the last two months (optionally filtered by category)."""
    d = df[df["type"] == "expense"].copy()
    if category:
        d = d[d["category"] == category]
    if d.empty:
        return None
    d["month"] = d["date"].dt.to_period("M")
    monthly = d.groupby("month")["amount"].sum().sort_index()
    if len(monthly) < 2:
        return None
    prev, curr = monthly.iloc[-2], monthly.iloc[-1]
    if prev == 0:
        return None
    return round(((curr - prev) / prev) * 100, 2)


def generate_insights(df: pd.DataFrame, portfolio_growth_pct: float | None = None) -> list[str]:
    """Human-readable monthly insight strings."""
    insights = []

    overall_change = month_over_month_change(df)
    if overall_change is not None:
        direction = "increased" if overall_change > 0 else "decreased"
        insights.append(f"Overall spending {direction} by {abs(overall_change)}% vs. last month.")

    for cat in df["category"].dropna().unique() if not df.empty else []:
        change = month_over_month_change(df, category=cat)
        if change is not None and abs(change) >= 10:
            direction = "increased" if change > 0 else "decreased"
            insights.append(f"{cat} spending {direction} by {abs(change)}% vs. last month.")

    ratio = savings_ratio(df)
    insights.append(f"Your current savings ratio is {ratio}% of income.")

    if portfolio_growth_pct is not None:
        direction = "grew" if portfolio_growth_pct >= 0 else "declined"
        insights.append(f"Investment portfolio {direction} by {abs(portfolio_growth_pct)}%.")

    if not insights:
        insights.append("Add some transactions to start seeing personalized insights.")

    return insights
