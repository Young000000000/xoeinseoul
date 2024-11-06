import streamlit as st
import pandas as pd

# Load data from CSV file
def load_data(filename="xoeinseoul.csv"):
    data = pd.read_csv(filename)
    return data

# Display the table of all data
def display_table(data):
    st.title("상품 데이터 테이블")
    st.write(data)

# Display the daily summary
def daily_summary(data):
    st.title("Daily Summary")
    
    # Convert '판매일' to datetime if not already
    data['판매일'] = pd.to_datetime(data['판매일']).dt.date
    
    # Calculate daily summary
    daily_summary = data.groupby('판매일').agg(
        판매량=('상품id', 'count'),
        총판매액=('판매가격', 'sum')
    ).reset_index()
    
    # Display daily summary
    st.write(daily_summary)

# Load data from CSV
data = load_data()

# Streamlit sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["상품 데이터 테이블", "Daily Summary"])

# Load appropriate page
if page == "상품 데이터 테이블":
    display_table(data)
elif page == "Daily Summary":
    daily_summary(data)