import streamlit as st
import pandas as pd

# Load data from CSV file
def load_data(filename="xoeinseoul.csv"):
    data = pd.read_csv(filename)
    data['구매확정일'] = pd.to_datetime(data['구매확정일']).dt.date  # Show only date for purchase_confirmed_at
    data['판매일'] = pd.to_datetime(data['판매일']).dt.date         # Show only date for created_at
    return data

# Display the daily summary with overall sum table
def display_daily_summary(data):
    st.title("Daily Summary")
    
    # Convert '판매일' to datetime if not already
    data['판매일'] = pd.to_datetime(data['판매일']).dt.date
    
    # Calculate daily summary
    daily_summary = data.groupby('판매일').agg(
        판매량=('상품id', 'count'),
        총판매액=('판매가격', 'sum')
    ).reset_index()
    
    # Calculate average price for each day without decimal
    daily_summary['평균 가격'] = (daily_summary['총판매액'] / daily_summary['판매량']).astype(int)
    
    # Format currency columns without decimals and with comma
    daily_summary['총판매액'] = daily_summary['총판매액'].apply(lambda x: f"{x:,}")
    daily_summary['평균 가격'] = daily_summary['평균 가격'].apply(lambda x: f"{x:,}")
    
    # Calculate overall summary
    total_sales_count = daily_summary['판매량'].sum()
    total_sales_amount = daily_summary['총판매액'].str.replace(',', '').astype(int).sum()
    overall_summary = pd.DataFrame({
        "전체 판매량": [total_sales_count],
        "전체 판매액": [f"{total_sales_amount:,}"],
        "전체 평균 가격": [f"{(total_sales_amount / total_sales_count):,.0f}"]
    })
    
    # Display overall summary at the top without index
    st.write("### 전체 판매 요약")
    st.dataframe(overall_summary, use_container_width=True)

    # Display daily summary table without index
    st.write("### 일별 판매 요약")
    st.dataframe(daily_summary, use_container_width=True)

# Display the full data table without index
def display_table(data):
    st.title("상품 데이터 테이블")
    # Format price column with commas and no decimals
    data['판매가격'] = data['판매가격'].apply(lambda x: f"{int(x):,}")
    st.dataframe(data.reset_index(drop=True), use_container_width=True)  # Remove index

# Load data from CSV
data = load_data()

# Create tabs with Daily Summary as the first tab
tab1, tab2 = st.tabs(["Daily Summary", "상품 데이터 테이블"])

with tab1:
    display_daily_summary(data)

with tab2:
    display_table(data)
