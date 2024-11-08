import streamlit as st
import pandas as pd

# Set the page layout to wide
st.set_page_config(layout="wide")

# Load data from CSV file
def load_data(filename="xoeinseoul.csv"):
    data = pd.read_csv(filename)
    data['구매확정일'] = pd.to_datetime(data['구매확정일']).dt.date  # Show only date for purchase_confirmed_at
    data['주문일'] = pd.to_datetime(data['주문일']).dt.date         # Show only date for created_at
    return data

# Display the summaries with columns for layout
def display_summaries(data):
    # Calculate daily summary
    daily_summary = data.groupby('주문일').agg(
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
    
    # Calculate monthly summary
    data['주문월'] = pd.to_datetime(data['주문일']).dt.to_period('M')
    monthly_summary = data.groupby('주문월').agg(
        판매량=('상품id', 'count'),
        총판매액=('판매가격', 'sum')
    ).reset_index()
    
    # Calculate average price for each month without decimal
    monthly_summary['평균 가격'] = (monthly_summary['총판매액'] / monthly_summary['판매량']).astype(int)
    
    # Format currency columns without decimals and with comma
    monthly_summary['총판매액'] = monthly_summary['총판매액'].apply(lambda x: f"{x:,}")
    monthly_summary['평균 가격'] = monthly_summary['평균 가격'].apply(lambda x: f"{x:,}")
    
    # Layout with two columns
    col1, col2 = st.columns(2)

    # Display overall and monthly summaries in the left column
    with col1:
        st.write("### 전체 판매 요약")
        st.write(overall_summary)
        st.write("### 월별 판매 요약")
        st.write(monthly_summary)

    # Display daily summary in the right column
    with col2:
        st.write("### 일별 판매 요약")
        st.write(daily_summary)

# Display the full data table without index, sorted by '주문일' in descending order
def display_table(data):
    # Sort by '주문일' in descending order
    data = data.sort_values(by='주문일', ascending=False).reset_index(drop=True)
    
    # Format price column with commas and no decimals
    data['판매가격'] = data['판매가격'].apply(lambda x: f"{int(x):,}")
    
    # Display the data table in wide mode without index
    st.dataframe(data, use_container_width=True)

# Load data from CSV
data = load_data()

# Create tabs with Daily Summary as the first tab
tab1, tab2 = st.tabs(["판매현황", "상품 데이터 테이블"])

with tab1:
    display_summaries(data)

with tab2:
    display_table(data)
