expense-tracker/
├── app/
│   └── dashboard.py          # Streamlit dashboard — reads from Supabase, deployed on Streamlit Cloud
├── src/
│   ├── plaid_client.py       # Main pipeline — Plaid sync, Gemini categorization, Supabase write
│   ├── llm_categorization.py # Gemini AI categorization function
│   ├── notifications.py      # Placeholder for future email alert logic
│   └── ml/
│       ├── train.py          # Placeholder for Phase II regression model training
│       └── predict.py        # Placeholder for Phase II spending predictions
├── processing/
│   └── cleaning.ipynb        # Exploratory data analysis and field selection
├── input/
│   └── raw/                  # Placeholder for raw JSON responses (not used in production)
├── output/                   # Local only — gitignored. Was SQLite storage before Supabase migration.
├── reference/
│   ├── assumptions.md        # Data field selection rationale and project assumptions
│   ├── file_structure.md     # This file
│   └── challenges.md         # Engineering challenges and learnings
├── .github/
│   └── workflows/
│       └── daily_sync.yml    # GitHub Actions cron job — runs plaid_client.py daily at 8AM UTC
├── .env                      # Local secrets — never committed (in .gitignore)
├── .gitignore                # Excludes .env, __pycache__, *.db
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview and setup instructions
