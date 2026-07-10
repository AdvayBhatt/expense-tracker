import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

#first write conn to db
output_dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(output_dir, "output", "expenses.db")
engine = create_engine(f"sqlite:///{db_path}")

df = pd.read_sql(sql = "SELECT * FROM transactions_tbl", con=engine)

st.title('Transactions Dashboard')

df['date'] = pd.to_datetime(df['date'])

df['year_month'] = df['date'].dt.strftime('%Y-%m')

sum_df = df.groupby('year_month').amount.sum()

st.subheader("Transaction Amount by Year-Month")

sum_df = sum_df.reset_index()
st.bar_chart(data=sum_df, y = 'amount', x = 'year_month')

st.write(df.columns.tolist())



category_df = df.groupby(['year_month', 'gemini_category'])['amount'].sum().unstack(fill_value=0) 
#unstack is used so that we don't get something like
#2026-06   Transport          $X
#          Food               $Y
#          Entertainment      $Z
#2026-05   Transport          $X
#          Food               $Y
#          Entertainment      $Z
#so we unstack by taking that inner list and pivoting it to columns

st.subheader("Transaction Amount Categorized")
st.bar_chart(category_df)

