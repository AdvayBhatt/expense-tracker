import streamlit as st
from supabase import create_client
import plotly.express as px
import pandas as pd
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
result = supabase.table("transactions").select("*").execute()
df = pd.DataFrame(result.data)

st.write("hello")
st.write(df.head())

df['date'] = pd.to_datetime(df['date'])
df['year_month'] = df['date'].dt.strftime('%Y-%m')
sum_df = df.groupby('year_month').amount.sum().reset_index()

fig = px.bar(sum_df, x="year_month", y="amount")
st.plotly_chart(fig, use_container_width=True)
st.write("chart done")