import streamlit as st
import pandas as pd
import os
from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.express as px
from supabase import create_client
from dotenv import load_dotenv

#first write conn to db
#output_dir = os.path.dirname(os.path.dirname(__file__))
#db_path = os.path.join(output_dir, "output", "expenses.db")
#engine = create_engine(f"sqlite:///{db_path}")

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

result = supabase.table("transactions").select("*").execute()

df = pd.DataFrame(result.data)
st.write(df.head())

st.title('Transactions Dashboard')

df['date'] = pd.to_datetime(df['date'])

df['year_month'] = df['date'].dt.strftime('%Y-%m')

sum_df = df.groupby('year_month').amount.sum()
sum_df = sum_df.reset_index()

bar_col1, bar_col2 = st.columns(2)
with bar_col1:
    st.subheader("Transaction Amount by Year-Month")

    

    fig = px.bar(
        sum_df,
        x="year_month",
        y="amount",
        labels={"year_month": "Month", "amount": "Amount ($)"}
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        xaxis_tickangle=-45,
        template="plotly_dark",
        xaxis_type="category"
    )

    st.plotly_chart(fig, use_container_width=True)

with bar_col2:
    st.subheader("Transaction Amount Categorized")

    category_df = (
        df.groupby(["year_month", "gemini_category"])["amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_df,
        x="year_month",
        y="amount",
        color="gemini_category",
        labels={
            "year_month": "Month",
            "amount": "Amount ($)",
            "gemini_category": "Category",
        },
    )

    fig.update_layout(
        barmode="stack",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        xaxis_tickangle=-45,
        template="plotly_dark",
        legend_title="Category",
        xaxis_type="category"
    )

    st.plotly_chart(fig, use_container_width=True)
#unstack is used so that we don't get something like
#2026-06   Transport          $X
#          Food               $Y
#          Entertainment      $Z
#2026-05   Transport          $X
#          Food               $Y
#          Entertainment      $Z
#so we unstack by taking that inner list and pivoting it to columns



# st.subheader("Transaction Amount by Year-Month")
# sum_df = sum_df.reset_index()
# st.bar_chart(data=sum_df, y = 'amount', x = 'year_month')

# category_df = df.groupby(['year_month', 'gemini_category'])['amount'].sum().unstack(fill_value=0) 
# st.subheader("Transaction Amount Categorized")
# st.bar_chart(category_df)

st.subheader("Transaction Amount by Year-Month Line Graph")

fig = px.line(
    sum_df,
    x="year_month",
    y="amount",
    labels={"year_month": "Month", "amount": "Amount ($)"}
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount ($)",
    xaxis_tickangle=-45,
    template="plotly_dark",
    xaxis_type="category"
)

st.plotly_chart(fig, use_container_width=True)

this_month_df = df[(df['date'].dt.year == date.today().year) & (df['date'].dt.month == date.today().month)]

this_week_df = df[(df['date'].dt.year == date.today().year) & (df['date'].dt.isocalendar().week == date.today().isocalendar().week)]

today_df = df[(df['date'].dt.day == date.today().day) & (df['date'].dt.year == date.today().year) & (df['date'].dt.month == date.today().month)]

prev_month = date.today() + relativedelta(months=-1)

prev_month_df = df[(df['date'].dt.year == prev_month.year) & (df['date'].dt.month == prev_month.month)]
delta_monthly_cost = this_month_df['amount'].sum() - prev_month_df['amount'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Latest Monthly Spend", f"${this_month_df['amount'].sum():,.2f}", f"-${abs(delta_monthly_cost):,.2f}" if delta_monthly_cost < 0 else f"${delta_monthly_cost:,.2f}", delta_color="inverse") 
with col2:
    st.metric("Latest Weekly Spend", f"${this_week_df['amount'].sum():,.2f}")
with col3:
    st.metric("Latest Daily Spend", f"${today_df['amount'].sum():,.2f}")

