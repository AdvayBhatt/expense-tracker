# Assumptions

## Data Field Selection

The Plaid API returns a large number of fields per transaction. The following documents which fields were kept, which were dropped, and why.

### Fields Kept

| Field | Reason |
|-------|--------|
| `transaction_id` | Unique identifier — used for deduplication |
| `account_id` | Identifies which account the transaction belongs to |
| `amount` | Core metric — spending amount |
| `date` | Primary date field for time-series analysis |
| `merchant_name` | Plaid's cleaned merchant name — preferred over raw `name` |
| `name` | Fallback when `merchant_name` is null |
| `payment_channel` | How the payment was made (in-store, online, other) |
| `pending` | Used to identify transactions not yet posted |
| `transaction_type` | Broad type classification |
| `personal_finance_category.primary` | Plaid's primary category (new taxonomy) |
| `personal_finance_category.detailed` | More granular Plaid category |
| `personal_finance_category.confidence_level` | Used to decide when to trust Plaid vs call Gemini |
| `location.city` | Geographic context for spending analysis |
| `location.country` | Geographic context |
| `gemini_category` | AI-assigned clean spending label (Food, Transport, Bills, etc.) |

### Fields Dropped

| Field | Reason |
|-------|--------|
| `authorized_date` / `authorized_datetime` | `date` is sufficient for spending analysis |
| `category` / `category_id` | Legacy Plaid taxonomy replaced by `personal_finance_category` |
| `check_number` | Rarely populated for consumer transactions |
| `counterparties` | Not needed for spending analysis |
| `iso_currency_code` / `unofficial_currency_code` | All transactions in USD |
| `logo_url` / `website` | UI metadata, not analytical |
| `merchant_entity_id` | Not needed when `merchant_name` is available |
| `payment_meta` | Too granular (payment processor, reference numbers) |
| `pending_transaction_id` | Only need to know if pending, not link to another transaction |
| `personal_finance_category.version` | Taxonomy metadata, not analytical |
| `transaction_code` | Mostly null for consumer transactions |
| `location.address` / `lat` / `lon` / `postal_code` / `region` / `store_number` | Granular location data not needed for current analysis |

---

## Categorization Assumptions

- Gemini is called for every transaction regardless of Plaid confidence level, to ensure consistent clean labels across all transactions
- Gemini is instructed to return exactly one of: Food, Transport, Entertainment, Shopping, Bills, Other
- Transfers, refunds, and credit card payments are included in the data since they are part of the real spending lifecycle
- Negative amounts represent credits or refunds — included but may skew monthly totals

---

## Pipeline Assumptions

- The Plaid sandbox is used for all development and demo purposes — no real bank accounts are connected
- A new Plaid Item (sandbox bank connection) is created on first run and the access token is stored in `.env`
- The cursor is not persisted between GitHub Actions runs — each run fetches all transactions, with deduplication handling repeated records
- Daily sync is sufficient given Plaid checks for new transactions 1-4 times per day depending on institution
