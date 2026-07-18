from google import genai
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv() #auto find env

#path
curr_dir = os.getcwd()
os_path = os.path.join(curr_dir, ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

#take in key data fields like merchant_name, primary_category, detailed_category and categorize using llm

def categorize_transaction(merchant_name, primary_category, detailed_category):                 
    
    response_1 = client.models.generate_content(         
        model="gemini-3.1-flash-lite",         
        contents= f"Given a transaction at '{merchant_name}' categorized as '{primary_category} - {detailed_category}', return a single clean spending category of exactly one of these categories and nothing else: Food, Transport, Entertainment, Shopping, Bills, or Other. Return only the category name, nothing else.") 
    sleep(4)
    return response_1.text

