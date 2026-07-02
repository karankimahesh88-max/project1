"""
Stock market data service.

Default: yfinance (free, no API key, good for a demo/learning project).
Optional: Alpha Vantage if ALPHA_VANTAGE_API_KEY is set in secrets (has a
strict 25 requests/day free-tier limit, so results are cached).
"""
import time
import requests
import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data(ttl=300, show_spinner=False)  # cache prices for 5 minutes
def get_current_price(symbol: str) -> dict:
    """Return current price + daily change % for a symbol. Raises on failure."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")
        if hist.empty:
            raise ValueError(f"No data found for symbol '{symbol}'. Check the ticker.")
        last_close = hist["Close"].iloc[-1]
        prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else last_close
        change_pct = ((last_close - prev_close) / prev_close) * 100 if prev_close else 0.0
        return {
            "symbol": symbol.upper(),
            "price": round(float(last_close), 2),
            "changePercent": round(float(change_pct), 2),
        }
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch price for {symbol}: {exc}") from exc


@st.cache_data(ttl=900, show_spinner=False)  # cache history for 15 minutes
def get_historical_data(symbol: str, period: str = "6mo") -> pd.DataFrame:
    """Return OHLC history for charting."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            raise ValueError(f"No historical data for '{symbol}'.")
        hist = hist.reset_index()
        return hist[["Date", "Open", "High", "Low", "Close", "Volume"]]
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch history for {symbol}: {exc}") from exc


@st.cache_data(ttl=3600, show_spinner=False)
def search_symbol(query: str) -> list[dict]:
    """Very light symbol search using Yahoo's public autocomplete endpoint."""
    try:
        resp = requests.get(
            "https://query2.finance.yahoo.com/v1/finance/search",
            params={"q": query, "quotesCount": 8, "newsCount": 0},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=6,
        )
        resp.raise_for_status()
        quotes = resp.json().get("quotes", [])
        return [
            {"symbol": q.get("symbol"), "name": q.get("shortname") or q.get("longname", "")}
            for q in quotes if q.get("symbol")
        ]
    except Exception:
        # Non-fatal: search is a convenience feature, fail quietly.
        return []


def get_prices_bulk(symbols: list[str]) -> dict[str, dict]:
    """Fetch prices for multiple symbols, skipping ones that fail (rate limit safe)."""
    results = {}
    for sym in symbols:
        try:
            results[sym] = get_current_price(sym)
        except RuntimeError:
            results[sym] = {"symbol": sym, "price": None, "changePercent": None}
        time.sleep(0.05)  # tiny delay to be polite to the API
    return results
