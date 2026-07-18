# Expense Tracker

An automated personal finance dashboard that pulls real bank transaction data, categorizes spending using AI, and visualizes habits over time.

**Live demo:** https://expense-tracker-6uytz4wayp84iajhvgvzkc.streamlit.app/

---

## What It Does

- Connects to bank accounts via the **Plaid API** to retrieve transaction history
- Uses **Gemini AI** to categorize each transaction into clean spending labels (Food, Transport, Bills, etc.)
- Stores transactions in **Supabase** (PostgreSQL) with deduplication to avoid double-counting
- Syncs automatically every day via **GitHub Actions**
- Displays spending trends, category breakdowns, and KPIs in a **Streamlit** dashboard deployed on Streamlit Cloud

---

## Architecture

```
Plaid API (sandbox)
    ↓
plaid_client.py — fetches transactions, runs Gemini categorization
    ↓
Supabase (PostgreSQL) — cloud database with deduplication
    ↓
GitHub Actions — triggers daily sync at 8AM UTC
    ↓
Streamlit Cloud — live dashboard reads from Supabase
```

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Data source | Plaid API (sandbox) |
| AI categorization | Google Gemini 3.1 Flash Lite |
| Database | Supabase (PostgreSQL) |
| Dashboard | Streamlit + Plotly |
| Scheduling | GitHub Actions (cron) |
| Deployment | Streamlit Community Cloud |
| Language | Python 3.11 |

---

## Key Design Decisions

**Cursor-based sync:** Plaid's `transactions/sync` endpoint uses a cursor to track which transactions have already been retrieved. On each run, you only get new transactions since the last sync are fetched, so the pipeline is efficient.

**AI categorization strategy:** Plaid provides its own category labels but with varying confidence levels. Gemini is called for every transaction to produce labels that will make sense (Food, Transport, Bills, Shopping, Entertainment, Other), replacing Plaid's raw codes.

**Deduplication:** Before writing to Supabase, existing `transaction_id` values are queried and new records are filtered to only actually new transactions, preventing duplicates across runs.

**Supabase over SQLite:** SQLite cannot persist data between GitHub Actions runs (stateless environment). Supabase provides a hosted PostgreSQL instance accessible from both the sync pipeline and the Streamlit dashboard.

---

## Project Structure

```
expense-tracker/
├── app/
│   └── dashboard.py          # Streamlit dashboard (deployed on Streamlit Cloud)
├── src/
│   ├── plaid_client.py       # Plaid API sync + Gemini categorization + Supabase write
│   ├── llm_categorization.py # Gemini AI categorization logic
│   ├── notifications.py      # Placeholder for future email alerts
│   └── ml/
│       ├── train.py          # Placeholder for Phase II regression model
│       └── predict.py        # Placeholder for Phase II predictions
├── processing/
│   └── cleaning.ipynb        # Exploratory data analysis notebook
├── reference/
│   ├── assumptions.md        # Data field selection rationale
│   ├── problems.md           # Engineering decisions log
│   └── file_structure.md     # Project structure notes
├── .github/
│   └── workflows/
│       └── daily_sync.yml    # GitHub Actions daily sync schedule
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.11+
- Plaid developer account (free sandbox)
- Google AI Studio account (free Gemini API key)
- Supabase account (free tier)

### Environment Variables

Create a `.env` file in the project root:

```
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_sandbox_secret
PLAID_ACCESS_ID=your_plaid_access_token
GEMINI_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_secret_key
```

### Installation

```bash
pip install -r requirements.txt
```

### Run the sync pipeline

```bash
python src/plaid_client.py
```

### Run the dashboard locally

```bash
streamlit run app/dashboard.py
```

---

## Dashboard Features

- **Monthly spend bar chart** — total spending per month
- **Category breakdown** — stacked bar chart showing spending by AI-assigned category per month
- **Spending trend** — line chart showing monthly spend over time
- **KPI cards** — latest monthly, weekly, and daily spend with month-over-month delta

---

## Planned Future Work (Phase II)

- **Linear regression model** to predict next month's spending based on category trends and contextual features (e.g., in-school vs summer)
- **Email notifications** via Gmail OAuth when monthly spending exceeds a defined threshold
- **Multiple bank account support** — extend pipeline to handle multiple Plaid Items (e.g., Bank of America + Citibank)
- **Real bank connection** — currently uses Plaid sandbox with synthetic transactions; production deployment would connect to real accounts
- **Spending recommendations** — AI-generated advice based on category trends

---

## Notes

- All transaction data shown in the live demo is synthetic (Plaid sandbox)
- Real bank credentials are never committed to the repository
- API keys are stored as GitHub Secrets for the Actions workflow and as Streamlit Secrets for the dashboard
