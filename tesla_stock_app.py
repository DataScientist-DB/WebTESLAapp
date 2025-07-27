import streamlit as st
from datetime import date
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Tesla Stock Tracker", layout="wide")
st.title("📈 Tesla (TSLA) Stock Tracker")



@st.cache_data
def load_tesla_data(start_date, end_date):
    df = yf.download("TSLA", start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

# Sidebar inputs
st.sidebar.header("Select date range")
today = date.today()
default_start = today.replace(year=today.year - 1)
start_date = st.sidebar.date_input("Start date", value=default_start)
end_date = st.sidebar.date_input("End date", value=today)

# Fetch data
data_load_state = st.text("Loading data...")
df = load_tesla_data(start_date, end_date)
data_load_state.text("Loading data... done.")

# Show summary and table
st.subheader(f"TSLA from {start_date} to {end_date}")
st.write(df.tail())

# Interactive chart
st.subheader("Closing Price Over Time")
st.line_chart(df.set_index("Date")["Close"])

# Additional statistics
st.subheader("Statistics")
st.write(df.describe())

# Optionally show volume or moving average
show_volume = st.sidebar.checkbox("Show Volume", value=False)
if show_volume:
    st.subheader("Volume")
    st.bar_chart(df.set_index("Date")["Volume"])

show_ma = st.sidebar.checkbox("Show 20‑day Moving Avg", value=False)
if show_ma:
    df["MA20"] = df["Close"].rolling(window=20).mean()
    st.subheader("Closing Price with 20‑day MA")
    chart_data = df.set_index("Date")[["Close", "MA20"]]
    st.line_chart(chart_data)
