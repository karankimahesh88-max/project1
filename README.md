# Personal Finance & Investment Tracker — Streamlit Edition

A Streamlit port of the React/Firebase finance tracker. Same data model and
feature set, running as a single Python app with Firebase as the backend.

## Folder structure
```
finance-tracker/
├── app.py                      # entry point, all pages + routing
├── requirements.txt
├── .streamlit/
│   └── secrets.toml.example    # copy to secrets.toml and fill in
├── services/
│   ├── firebase_service.py     # Admin SDK + Firestore client
│   ├── auth_service.py         # sign up / sign in / session
│   ├── db_service.py           # Firestore CRUD (transactions, investments, goals)
│   └── stock_service.py        # yfinance-backed stock data
├── utils/
│   └── analytics.py            # monthly insights, trends, savings ratio
└── components/
    └── charts.py                # Plotly chart builders
```

## 1. Firebase setup
1. Create a Firebase project at https://console.firebase.google.com
2. Enable **Authentication → Sign-in method → Email/Password**
3. Create a **Firestore database** (production or test mode)
4. Get your **Web API key**: Project settings → General → "Web API Key"
5. Generate a **service account key**: Project settings → Service accounts →
   "Generate new private key" (downloads a JSON file)

## 2. Configure secrets
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Edit `.streamlit/secrets.toml`:
- Paste your Web API key into `FIREBASE_WEB_API_KEY`
- Paste the full contents of the downloaded service-account JSON into
  `FIREBASE_SERVICE_ACCOUNT_JSON` (as a triple-quoted string)

**Never commit `secrets.toml` to git** — it contains your service account's
private key.

## 3. Install & run
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
The app opens at `http://localhost:8501`.

## 4. Firestore security rules (recommended)
Since all writes go through the trusted Admin SDK on your server, you can
lock client-side access down entirely:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false; // only the Admin SDK (server) can touch data
    }
  }
}
```

## Notes on the stock API
This version uses **yfinance** (free, no API key, pulls from Yahoo Finance)
instead of Alpha Vantage/Finnhub, since Alpha Vantage's free tier is limited
to 25 requests/day, which is too restrictive for a live dashboard. Prices are
cached for 5 minutes and historical data for 15 minutes to avoid hammering
the API. If you'd rather use Alpha Vantage, swap the implementation in
`services/stock_service.py` — the `ALPHA_VANTAGE_API_KEY` secret slot is
already reserved for it.

Use standard ticker symbols, e.g. `AAPL`, `MSFT`, or `INFY.NS` for NSE-listed
Indian stocks.

## Deploying
- **Streamlit Community Cloud**: push this repo, add the same secrets in the
  app's "Secrets" settings panel, deploy.
- Any host that can run `streamlit run app.py` (Render, Railway, a VM, etc.)
  works the same way — just set the secrets as environment/secrets config.
