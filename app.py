"""
Personal Finance & Investment Tracker — Streamlit version.

Run with:  streamlit run app.py

Requires .streamlit/secrets.toml (see secrets.toml.example) with:
  FIREBASE_WEB_API_KEY
  FIREBASE_SERVICE_ACCOUNT_JSON
"""
import streamlit as st
import pandas as pd
from datetime import date, datetime

from services import auth_service, db_service, stock_service
from utils import analytics
from components import charts

st.set_page_config(page_title="Finance & Investment Tracker", page_icon="💰", layout="wide")

CURRENCY_SYMBOLS = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£"}


# ----------------------------------------------------------------------------
# Auth screens
# ----------------------------------------------------------------------------
def render_auth_screen():
    st.title("💰 Personal Finance & Investment Tracker")
    tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pw")
            submitted = st.form_submit_button("Log in", use_container_width=True)
        if submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                try:
                    data = auth_service.sign_in(email, password)
                    auth_service.start_session(data)
                    st.rerun()
                except ValueError as e:
                    st.error(f"Login failed: {e}")

    with tab_signup:
        with st.form("signup_form"):
            name = st.text_input("Display name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password (min 6 characters)", type="password", key="signup_pw")
            submitted = st.form_submit_button("Create account", use_container_width=True)
        if submitted:
            if not email or len(password) < 6:
                st.error("Enter a valid email and a password of at least 6 characters.")
            else:
                try:
                    data = auth_service.sign_up(email, password, name)
                    auth_service.start_session(data)
                    st.success("Account created!")
                    st.rerun()
                except ValueError as e:
                    st.error(f"Sign up failed: {e}")


# ----------------------------------------------------------------------------
# Data helpers
# ----------------------------------------------------------------------------
def compute_portfolio(uid: str) -> pd.DataFrame:
    inv_df = db_service.get_investments(uid)
    if inv_df.empty:
        return inv_df
    prices = stock_service.get_prices_bulk(inv_df["symbol"].unique().tolist())
    inv_df["currentPrice"] = inv_df["symbol"].map(lambda s: prices.get(s, {}).get("price"))
    inv_df["dayChangePct"] = inv_df["symbol"].map(lambda s: prices.get(s, {}).get("changePercent"))
    inv_df["purchaseValue"] = inv_df["purchasePrice"] * inv_df["quantity"]
    inv_df["currentValue"] = inv_df["currentPrice"] * inv_df["quantity"]
    inv_df["profitLoss"] = inv_df["currentValue"] - inv_df["purchaseValue"]
    inv_df["growthPct"] = (inv_df["profitLoss"] / inv_df["purchaseValue"]) * 100
    return inv_df


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_dashboard(uid: str, currency: str):
    st.header("📊 Dashboard")
    df = db_service.get_transactions(uid)
    portfolio_df = compute_portfolio(uid)
    sym = CURRENCY_SYMBOLS.get(currency, currency)

    total_income = df.loc[df["type"] == "income", "amount"].sum() if not df.empty else 0
    total_expense = df.loc[df["type"] == "expense", "amount"].sum() if not df.empty else 0
    total_savings = total_income - total_expense
    portfolio_value = portfolio_df["currentValue"].sum() if not portfolio_df.empty else 0
    portfolio_growth = (
        (portfolio_df["profitLoss"].sum() / portfolio_df["purchaseValue"].sum() * 100)
        if not portfolio_df.empty and portfolio_df["purchaseValue"].sum() > 0 else 0
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Income", f"{sym}{total_income:,.0f}")
    c2.metric("Total Expenses", f"{sym}{total_expense:,.0f}")
    c3.metric("Total Savings", f"{sym}{total_savings:,.0f}")
    c4.metric("Portfolio Value", f"{sym}{portfolio_value:,.0f}")
    c5.metric("Portfolio Growth", f"{portfolio_growth:,.2f}%")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        fig = charts.expense_pie_chart(analytics.category_breakdown(df))
        st.plotly_chart(fig, use_container_width=True) if fig else st.info("No expenses yet.")
    with col2:
        fig = charts.monthly_bar_chart(analytics.monthly_totals(df))
        st.plotly_chart(fig, use_container_width=True) if fig else st.info("No transactions yet.")

    col3, col4 = st.columns(2)
    with col3:
        fig = charts.spending_trend_line(analytics.monthly_totals(df))
        st.plotly_chart(fig, use_container_width=True) if fig else st.info("No spending trend yet.")
    with col4:
        st.subheader("Top performing stock")
        if not portfolio_df.empty:
            top = portfolio_df.sort_values("growthPct", ascending=False).iloc[0]
            st.metric(top["symbol"], f"{sym}{top['currentValue']:,.0f}", f"{top['growthPct']:.2f}%")
        else:
            st.info("Add an investment to see top performers.")

    st.divider()
    st.subheader("Recent transactions")
    st.dataframe(
        df.head(8)[["date", "type", "category", "description", "amount"]] if not df.empty else df,
        use_container_width=True, hide_index=True,
    )

    st.subheader("Goal progress")
    goals_df = db_service.get_goals(uid)
    if goals_df.empty:
        st.info("No goals set yet — add one in the Goals tab.")
    else:
        for _, g in goals_df.iterrows():
            frac = charts.goal_progress_bar(g["currentAmount"], g["targetAmount"])
            st.write(f"**{g['title']}** — {sym}{g['currentAmount']:,.0f} / {sym}{g['targetAmount']:,.0f}")
            st.progress(frac)

    st.subheader("💡 Monthly insights")
    for tip in analytics.generate_insights(df, portfolio_growth if not portfolio_df.empty else None):
        st.write(f"- {tip}")


def page_transactions(uid: str, currency: str):
    st.header("🧾 Transactions")
    sym = CURRENCY_SYMBOLS.get(currency, currency)

    with st.expander("➕ Add a transaction", expanded=True):
        with st.form("add_tx_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            tx_type = c1.selectbox("Type", ["expense", "income"])
            category = c2.selectbox("Category", db_service.CATEGORIES)
            amount = c3.number_input("Amount", min_value=0.0, step=100.0)
            c4, c5 = st.columns(2)
            description = c4.text_input("Description")
            tx_date = c5.date_input("Date", value=date.today())
            submitted = st.form_submit_button("Add transaction")
        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than 0.")
            else:
                db_service.add_transaction(
                    uid, amount, category, tx_type, description, tx_date.isoformat()
                )
                st.success("Transaction added.")
                st.rerun()

    df = db_service.get_transactions(uid)
    st.subheader("Filter & search")
    c1, c2, c3 = st.columns(3)
    type_filter = c1.multiselect("Type", ["income", "expense"], default=["income", "expense"])
    cat_filter = c2.multiselect("Category", db_service.CATEGORIES, default=db_service.CATEGORIES)
    search = c3.text_input("Search description")

    filtered = df[df["type"].isin(type_filter) & df["category"].isin(cat_filter)] if not df.empty else df
    if search and not filtered.empty:
        filtered = filtered[filtered["description"].str.contains(search, case=False, na=False)]

    # Pagination
    page_size = 10
    total_rows = len(filtered)
    total_pages = max(1, (total_rows - 1) // page_size + 1)
    page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    start, end = (page_num - 1) * page_size, page_num * page_size
    page_df = filtered.iloc[start:end]

    st.caption(f"Showing {min(end, total_rows)} of {total_rows} transactions")
    for _, row in page_df.iterrows():
        cols = st.columns([2, 2, 2, 3, 2, 1, 1])
        cols[0].write(row["date"].strftime("%Y-%m-%d") if pd.notna(row["date"]) else "")
        cols[1].write(row["type"])
        cols[2].write(row["category"])
        cols[3].write(row["description"])
        cols[4].write(f"{sym}{row['amount']:,.2f}")
        if cols[5].button("✏️", key=f"edit_{row['id']}"):
            st.session_state["editing_tx"] = row["id"]
        if cols[6].button("🗑️", key=f"del_{row['id']}"):
            db_service.delete_transaction(uid, row["id"])
            st.rerun()

    # Inline edit form
    if st.session_state.get("editing_tx"):
        tx_id = st.session_state["editing_tx"]
        tx_row = df[df["id"] == tx_id].iloc[0]
        st.subheader("Edit transaction")
        with st.form("edit_tx_form"):
            new_amount = st.number_input("Amount", value=float(tx_row["amount"]))
            new_category = st.selectbox(
                "Category", db_service.CATEGORIES,
                index=db_service.CATEGORIES.index(tx_row["category"])
                if tx_row["category"] in db_service.CATEGORIES else 0,
            )
            new_desc = st.text_input("Description", value=tx_row["description"])
            save = st.form_submit_button("Save changes")
            cancel = st.form_submit_button("Cancel")
        if save:
            db_service.update_transaction(
                uid, tx_id, amount=new_amount, category=new_category, description=new_desc
            )
            st.session_state.pop("editing_tx")
            st.rerun()
        if cancel:
            st.session_state.pop("editing_tx")
            st.rerun()


def page_investments(uid: str, currency: str):
    st.header("📈 Investments")
    sym = CURRENCY_SYMBOLS.get(currency, currency)

    with st.expander("🔍 Search a stock symbol"):
        query = st.text_input("Company name or symbol")
        if query:
            results = stock_service.search_symbol(query)
            for r in results:
                st.write(f"**{r['symbol']}** — {r['name']}")

    with st.expander("➕ Add an investment", expanded=True):
        with st.form("add_inv_form", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns(4)
            symbol = c1.text_input("Symbol (e.g. AAPL, INFY.NS)")
            quantity = c2.number_input("Quantity", min_value=0.0, step=1.0)
            purchase_price = c3.number_input("Purchase Price", min_value=0.0, step=1.0)
            purchase_date = c4.date_input("Purchase Date", value=date.today())
            submitted = st.form_submit_button("Add investment")
        if submitted:
            if not symbol or quantity <= 0 or purchase_price <= 0:
                st.error("Enter a valid symbol, quantity, and purchase price.")
            else:
                try:
                    stock_service.get_current_price(symbol)  # validates the symbol exists
                    db_service.add_investment(
                        uid, symbol, quantity, purchase_price, purchase_date.isoformat()
                    )
                    st.success(f"Added {symbol.upper()}.")
                    st.rerun()
                except RuntimeError as e:
                    st.error(str(e))

    portfolio_df = compute_portfolio(uid)
    if portfolio_df.empty:
        st.info("No investments yet — add one above.")
        return

    st.subheader("Holdings")
    for _, row in portfolio_df.iterrows():
        with st.container(border=True):
            c1, c2, c3, c4, c5, c6 = st.columns([2, 2, 2, 2, 2, 1])
            c1.write(f"**{row['symbol']}**")
            c2.write(f"Qty: {row['quantity']}")
            c3.write(f"Current: {sym}{row['currentPrice']:.2f}" if pd.notna(row["currentPrice"]) else "Current: N/A")
            pl_color = "🟢" if row["profitLoss"] >= 0 else "🔴"
            c4.write(f"{pl_color} P/L: {sym}{row['profitLoss']:,.2f}")
            c5.write(f"Growth: {row['growthPct']:.2f}%")
            if c6.button("🗑️", key=f"del_inv_{row['id']}"):
                db_service.delete_investment(uid, row["id"])
                st.rerun()

    st.subheader("Price history")
    chosen = st.selectbox("Symbol", portfolio_df["symbol"].unique())
    period = st.select_slider("Period", options=["1mo", "3mo", "6mo", "1y", "2y", "5y"], value="6mo")
    try:
        hist = stock_service.get_historical_data(chosen, period)
        fig = charts.portfolio_growth_chart(hist, chosen)
        st.plotly_chart(fig, use_container_width=True)
    except RuntimeError as e:
        st.error(str(e))


def page_goals(uid: str, currency: str):
    st.header("🎯 Financial Goals")
    sym = CURRENCY_SYMBOLS.get(currency, currency)

    with st.expander("➕ Add a goal", expanded=True):
        with st.form("add_goal_form", clear_on_submit=True):
            title = st.text_input("Goal title (e.g. 'Save for emergency fund')")
            c1, c2 = st.columns(2)
            target = c1.number_input("Target amount", min_value=0.0, step=1000.0)
            deadline = c2.date_input("Deadline")
            submitted = st.form_submit_button("Create goal")
        if submitted:
            if not title or target <= 0:
                st.error("Enter a title and a target amount greater than 0.")
            else:
                db_service.add_goal(uid, title, target, deadline.isoformat())
                st.success("Goal created.")
                st.rerun()

    goals_df = db_service.get_goals(uid)
    if goals_df.empty:
        st.info("No goals yet — create one above.")
        return

    for _, g in goals_df.iterrows():
        with st.container(border=True):
            st.write(f"**{g['title']}** — deadline {g['deadline']}")
            frac = charts.goal_progress_bar(g["currentAmount"], g["targetAmount"])
            st.progress(frac, text=f"{sym}{g['currentAmount']:,.0f} / {sym}{g['targetAmount']:,.0f} ({frac*100:.1f}%)")
            c1, c2 = st.columns([3, 1])
            new_val = c1.number_input(
                "Update current amount", value=float(g["currentAmount"]), key=f"goal_{g['id']}"
            )
            if c1.button("Save progress", key=f"save_goal_{g['id']}"):
                db_service.update_goal_progress(uid, g["id"], new_val)
                st.rerun()
            if c2.button("Delete", key=f"del_goal_{g['id']}"):
                db_service.delete_goal(uid, g["id"])
                st.rerun()


def page_settings(uid: str, prefs: dict):
    st.header("⚙️ Settings")
    st.subheader("Personalization")
    dark_mode = st.toggle("Dark mode (visual preference, saved to your profile)", value=prefs.get("darkMode", False))
    currency = st.selectbox(
        "Currency", list(CURRENCY_SYMBOLS.keys()),
        index=list(CURRENCY_SYMBOLS.keys()).index(prefs.get("currency", "INR")),
    )
    if st.button("Save preferences"):
        db_service.update_preferences(uid, darkMode=dark_mode, currency=currency,
                                       widgetOrder=prefs.get("widgetOrder", []))
        st.success("Preferences saved.")
        st.rerun()

    if dark_mode:
        st.markdown(
            "<style>.stApp{background-color:#0e1117;color:#fafafa;}</style>",
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------------
# Main router
# ----------------------------------------------------------------------------
def main():
    if not auth_service.is_authenticated():
        render_auth_screen()
        return

    user = auth_service.current_user()
    uid = user["uid"]
    prefs = db_service.get_preferences(uid) or {}
    currency = prefs.get("currency", "INR")

    if prefs.get("darkMode"):
        st.markdown("<style>.stApp{background-color:#0e1117;color:#fafafa;}</style>", unsafe_allow_html=True)

    with st.sidebar:
        st.title("💰 Finance Tracker")
        st.caption(f"Logged in as {user['email']}")
        page = st.radio("Navigate", ["Dashboard", "Transactions", "Investments", "Goals", "Settings"])
        st.divider()
        if st.button("Log out", use_container_width=True):
            auth_service.logout()
            st.rerun()

    try:
        if page == "Dashboard":
            page_dashboard(uid, currency)
        elif page == "Transactions":
            page_transactions(uid, currency)
        elif page == "Investments":
            page_investments(uid, currency)
        elif page == "Goals":
            page_goals(uid, currency)
        elif page == "Settings":
            page_settings(uid, prefs)
    except Exception as e:
        st.error(f"Something went wrong: {e}")


if __name__ == "__main__":
    main()
