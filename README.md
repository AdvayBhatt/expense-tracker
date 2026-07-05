The project here is an expense tracker employs the Plaid API to get expense data. I will craft this project with a outcome-focused roadmap:

1. Scope:
- I am seeking to answer various questions about my personal finance: How much do I spend per month? How can I categorize it (food, rent, entertainment, etc...)? What does the trend of my spending look like over time? How do my expenses compare to my income? How can I visualize my spending habits?
- metrics include monthly spending, category of spending, trending of expenses, some estimated threshold ratio of expenses to income
- expected decisions: cut back on highest unnecessary category if trend is increasing in cost and/or my expenses threshold ratio is too high
- goal: help me identify inefficent spending habits and optimize income

2. Process
- I aim to split the process into two phases
- PHASE I:
 - I will use Plaid API to retrieve expenses (for demo purposes, the data will be fake transactions)
 - I will create infrastructure to demonstrate continual retrieval of banking data remains stable
 - I will then create an interface (like Streamlit) to add various visuals using the metrics as thresholds
 - When those threshold are not met, have systems to send notifications
- PHASE II:
 - I may use linear regression (features: category, maybe binary variable like in_school, card type, etc..; target: monthly spending cost) to predict future spending
 - I will show preprocessing, training, eval, deployment, notes, and one-page business case
 - I will build a lightweight pipeline: ingest → preprocess → train → serve → monitor.
 - I will include signifigance testing, A/B testing, randomization, and discussions of Type I, Type II, and power where necessary
- END: I will include a "how to implement in production" section with data refresh cadence, monitoring metric, and rollback criteria

3. Production readiness
- Eventually would like maintainable system running at scale daily across users. Will use model versioning, testing, CI/CD, containerization, and performance monitoring.
- See if other tools are needed: Docker and a minimal monitoring stack (alert on feature drift or data schema changes)
- Need monitoring so the model doesn’t degrade: Implement a basic dashboard tracking prediction distributions and key input statistics.


4. Business fluency and data storytelling
- I will build a one-page dashboard focused on visualizing my spending habits and a one-slide executive summary with clear next steps.
- I will add a clear “recommended action” and a short implementation plan to every deliverable
- I will provide validation examples, a rollback plan, and a small pilot with control groups.
- I will practice framing project as business questions: Did new spending strategy over one period increase the amount saved? 


5. Ethics, governance & measurement
- Include privacy & security checks for the project (data protection, ensuring no data leakage, compliance)
- Define a simple measurement plan for each model: baseline metric, expected uplift, experiment duration, and success criteria.
- For each project, prototype a minimal viable product (MVP) to show early signals. For every project, include a one-page “risks & mitigations” with data lineage, privacy concerns, and rollback triggers. 


# File Structure

expense-tracker/
├─ input/
│  └─ raw/                    #raw JSON responses from Plaid API
├─ processing/
│  └─ cleaning.ipynb          #exploratory cleaning, visible output
├─ output/
│  └─ expenses.db             #SQLite database, clean processed data
├─ src/
│  ├─ plaid_client.py         #Plaid API calls
│  ├─ notifications.py        #alert/notification logic
│  └─ ml/
│     ├─ train.py             #model training
│     └─ predict.py           #model inference
├─ app/
│  └─ dashboard.py            #Streamlit app
├─ reference/
│  └─ assumptions.md          #project assumptions, data notes
├─ .env                       #API keys, never committed
├─ .gitignore                 #includes .env, __pycache__, .db optionally
├─ requirements.txt
└─ README.md

