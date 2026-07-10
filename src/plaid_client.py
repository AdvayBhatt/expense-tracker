import dotenv
from dotenv import load_dotenv
import pandas as pd
import os #need to handle env variables this way
import sys
sys.path.append(os.path.dirname(__file__))
import plaid
from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from time import sleep
from sqlalchemy import create_engine
from llm_categorization import categorize_transaction


load_dotenv() #finds .env file automatically actually if in root of project; don't need a path specified

#print(f"ACCESS_ID loaded: {os.getenv('PLAID_ACCESS_ID')}")

curr_dir = os.getcwd()
dotenv_path = os.path.join(curr_dir, ".env")

CLIENT_ID = os.getenv("PLAID_CLIENT_ID") #team id which acts as identifier
SECRET_ID = os.getenv("PLAID_SECRET") #specific id which acts as identifier
ACCESS_ID = os.getenv("PLAID_ACCESS_ID")


configuration = plaid.Configuration( #below is the client which is just a connection object
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': CLIENT_ID,
        'secret': SECRET_ID,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client) #main client name

#here we have a fake instituion then initial_products of which we just need transactions
pt_request = SandboxPublicTokenCreateRequest(
    institution_id="ins_109508",
    initial_products=[Products('transactions')]
)
if not ACCESS_ID:
    pt_response = client.sandbox_public_token_create(pt_request)
    # The generated public_token can now be
    # exchanged for an access_token
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=pt_response['public_token']
    )
    exchange_response = client.item_public_token_exchange(exchange_request)
    dotenv.set_key(dotenv_path, "PLAID_ACCESS_ID", exchange_response['access_token'])
    ACCESS_ID = exchange_response['access_token']
    sleep(3)

# Provide a cursor from your database if you've previously
# received one for the Item. Leave null if this is your
# first sync call for this Item. The first request will
# return a cursor.
CURSOR_ID = os.getenv("CURSOR_ID")

#only need added transactions
added = []

has_more = True

# Iterate through each page of new transaction updates for item
while has_more:
    if CURSOR_ID:
        request = TransactionsSyncRequest(
            access_token=ACCESS_ID,
            cursor=CURSOR_ID,
        )
    else:
        request = TransactionsSyncRequest(
            access_token=ACCESS_ID
        ) 
   
    response = client.transactions_sync(request)

    # Add this page of results
    added.extend(response['added'])

    has_more = response['has_more']

    # Update cursor to the next cursor
    CURSOR_ID = response['next_cursor']
    dotenv.set_key(dotenv_path, "CURSOR_ID", CURSOR_ID)

#no db right now

# method to convert 'added' list into pd dataframe

def transaction_func(added):
    cleaned = []
    for transaction in added:
        
        clean_dict = {
            "account_id": transaction["account_id"],
            "amount": transaction["amount"],
            "date": transaction["date"],
            "merchant_name": transaction["merchant_name"]
            if transaction.get("merchant_name") else transaction.get('name'),
            "payment_channel": transaction["payment_channel"],
            "pending": transaction["pending"],
            "transaction_id": transaction["transaction_id"],
            "transaction_type": transaction["transaction_type"],

            # nested fields
            "primary_category": transaction["personal_finance_category"]["primary"]
            if transaction.get("personal_finance_category") else None,

            "detailed_category": transaction["personal_finance_category"]["detailed"]
            if transaction.get("personal_finance_category") else None,

            "confidence_level": transaction["personal_finance_category"]["confidence_level"]
            if transaction.get("personal_finance_category") else None,

            # location (example)
            "city": transaction["location"]["city"]
            if transaction.get('location') else None,
            "country": transaction["location"]["country"]
            if transaction.get('location') else None,
        }
        
        cleaned.append(clean_dict)
    return pd.DataFrame(cleaned)

df = transaction_func(added)

df['gemini_category'] = df[['merchant_name', 'primary_category', 'detailed_category', 'confidence_level']].apply(
lambda row: categorize_transaction(row['merchant_name'], row['primary_category'], row['detailed_category']) if row['confidence_level'] == "LOW" else row['detailed_category'], 
axis=1) #need three columns for categorization use apply row so that we don't feed three seperate inputs (cols) to apply as a Series and instead put in one thing (each row) to operate on

print(df[['merchant_name', 'gemini_category']].head(10))

if not df.empty:
    output_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(output_dir, "output", "expenses.db")
    engine = create_engine(f"sqlite:///{db_path}")
    try:
        existing_transactions = pd.read_sql(sql = "SELECT transaction_id FROM transactions_tbl", con=engine)
    except:
        existing_transactions = pd.DataFrame(columns=['transaction_id'])
    df = df[~df['transaction_id'].isin(list(existing_transactions['transaction_id'].values))]
    print(f"Rows to write: {len(df)}")
    print(f"Existing rows: {len(existing_transactions)}")
    df.to_sql(name='transactions_tbl', con=engine,if_exists='append')
    print(pd.read_sql("SELECT COUNT(*) FROM transactions_tbl", con=engine))
