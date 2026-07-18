# Challenges & Learnings

## Engineering Challenges

### 1. Cursor persistence in stateless environments
**Problem:** The Plaid `transactions/sync` cursor tracks which transactions have already been fetched. Locally this was stored in `.env` via `dotenv.set_key()`. In GitHub Actions (stateless), the file system resets after each run so the cursor was lost.

**Solution:** Dropped cursor persistence entirely for the cloud pipeline. Each GitHub Actions run fetches all transactions from the beginning, and the deduplication logic (checking existing `transaction_id` values in Supabase) prevents duplicates. Slightly less efficient but correct and simple.

**Learning:** In stateless cloud environments, application state must live in an external persistent store, not the local file system.

---

### 2. SQLite → Supabase migration
**Problem:** SQLite databases are local files. They work fine for local development but cannot be shared between GitHub Actions (sync pipeline) and Streamlit Cloud (dashboard). Both need to read and write the same data.

**Solution:** Migrated to Supabase (hosted PostgreSQL). The schema was recreated in Supabase and the Python code was updated to use the Supabase client instead of SQLAlchemy + SQLite.

**Learning:** For any project with multiple compute environments accessing the same data, a hosted database is required from the start.

---

### 3. Gemini API rate limiting
**Problem:** Calling Gemini once per transaction in a batch of 50 immediately hit the free tier rate limit (requests per minute and per day).

**Solution:** Added `sleep(4)` between each Gemini call to stay under 15 requests per minute. Also switched from `gemini-2.0-flash` (exhausted quota) to `gemini-3.1-flash-lite` which has 500 requests per day on the free tier.

**Learning:** Always check rate limits before designing a batched API call pattern. Build in delays proactively.

---

### 4. Supabase column name mismatches
**Problem:** The Supabase table was initially designed with column names like `location_city` and `category_primary`, but the pandas DataFrame used `city` and `primary_category`. The insert failed with a schema cache error.

**Solution:** Dropped and recreated the Supabase table with column names exactly matching the DataFrame columns.

**Learning:** Define the database schema from the DataFrame columns, not the other way around. Mismatches between application and database naming are a common source of bugs.

---

### 5. JSON serialization of Python date objects
**Problem:** When converting the DataFrame to a list of dicts for Supabase insertion, the `date` column contained Python `datetime.date` objects which are not JSON serializable, causing an `httpx` encoding error.

**Solution:** Added `df['date'] = df['date'].astype(str)` before `df.to_dict('records')` to convert dates to ISO format strings.

**Learning:** Always convert non-primitive types (dates, decimals, numpy types) to strings or native Python types before JSON serialization.

---

### 6. Streamlit blank page (ad blocker)
**Problem:** Streamlit dashboard rendered completely blank with no errors in the terminal. The browser console showed a WebSocket connection being established but no content rendering.

**Solution:** The ad blocker (uBlock Origin) was intercepting WebSocket traffic on localhost even when "paused" for the page. Fully disabling the extension allowed the app to render. For Streamlit Cloud deployment the issue does not exist.

**Learning:** WebSocket-based apps (Streamlit, Jupyter) are commonly blocked by ad blockers on localhost. Always test with extensions disabled when debugging blank page issues.

---

## Key Technical Decisions

| Decision | Chosen | Rejected | Reason |
|----------|--------|----------|--------|
| Database | Supabase (PostgreSQL) | SQLite | SQLite can't persist between cloud runs |
| AI model | Gemini 3.1 Flash Lite | OpenAI GPT | Free tier, no credit card required |
| Dashboard | Streamlit | Power BI, Plotly Dash | Python-native, easy deployment |
| Scheduling | GitHub Actions | AWS Lambda, cron | Free, no account setup, repo-integrated |
| Charts | Plotly | Matplotlib, st.bar_chart | Better dark theme support, interactivity |
| API sync | transactions/sync (cursor) | transactions/get | Recommended by Plaid for new implementations |
