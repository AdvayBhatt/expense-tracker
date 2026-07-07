from dotenv import load_dotenv
import pandas as pd
import os #need to handle env variables this way
import plaid
from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from time import sleep

load_dotenv() #finds .env file automatically actually if in root of project; don't need a path specified

CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
SECRET_ID = os.getenv("PLAID_SECRET")



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
pt_response = client.sandbox_public_token_create(pt_request)
# The generated public_token can now be
# exchanged for an access_token
exchange_request = ItemPublicTokenExchangeRequest(
    public_token=pt_response['public_token']
)
exchange_response = client.item_public_token_exchange(exchange_request)
sleep(3)

# Provide a cursor from your database if you've previously
# received one for the Item. Leave null if this is your
# first sync call for this Item. The first request will
# return a cursor.
cursor = None

#only need added transactions
added = []

has_more = True

# Iterate through each page of new transaction updates for item
while has_more:
    if cursor:
        request = TransactionsSyncRequest(
            access_token=exchange_response['access_token'],
            cursor=cursor,
        )
    else:
        request = TransactionsSyncRequest(
            access_token=exchange_response['access_token']
        ) 
   
    response = client.transactions_sync(request)

    # Add this page of results
    added.extend(response['added'])

    has_more = response['has_more']

    # Update cursor to the next cursor
    cursor = response['next_cursor']

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