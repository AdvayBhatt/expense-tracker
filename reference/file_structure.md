expense-tracker/
├─ input/
│  └─ raw/                    # raw JSON responses from Plaid API
├─ processing/
│  └─ cleaning.ipynb          # exploratory cleaning, visible output
├─ output/
│  └─ expenses.db             # SQLite database, clean processed data
├─ src/
│  ├─ plaid_client.py         # Plaid API calls
│  ├─ notifications.py        # alert/notification logic
│  └─ ml/
│     ├─ train.py             # model training
│     └─ predict.py           # model inference
├─ app/
│  └─ dashboard.py            # Streamlit app
├─ reference/
│  └─ assumptions.md          # project assumptions, data notes
├─ .env                       # API keys, never committed
├─ .gitignore                 # includes .env, __pycache__, .db optionally
├─ requirements.txt
└─ README.md