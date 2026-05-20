import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Food Delivery Analytics Dashboard",
    page_icon="🍔",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data

def load_data():
    df = pd.read_csv("Final_dataset.csv")
    return df


df = load_data()

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = df.columns.str.strip()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filter Dashboard")

# City Filter
if 'City' in df.columns:
    city = st.sidebar.multiselect(
        "Select City",
        options=df['City'].dropna().unique(),
        default=df['City'].dropna().unique()
    )
    df = df[df['City'].isin(city)]

# Cuisine Filter
if 'Cuisine_Type' in df.columns:
    cuisine = st.sidebar.multiselect(
        "Select Cuisine",
        options=df['Cuisine_Type'].dropna().unique(),
        default=df['Cuisine_Type'].dropna().unique()
    )
    df = df[df['Cuisine_Type'].isin(cuisine)]

# Order Status Filter
if 'Order_Status' in df.columns:
    status = st.sidebar.multiselect(
        "Select Order Status",
        options=df['Order_Status'].dropna().unique(),
        default=df['Order_Status'].dropna().unique()
    )
    df = df[df['Order_Status'].isin(status)]

# Payment Mode Filter
if 'Payment_Mode' in df.columns:
    payment = st.sidebar.multiselect(
        "Select Payment Mode",
        options=df['Payment_Mode'].dropna().unique(),
        default=df['Payment_Mode'].dropna().unique()
    )
    df = df[df['Payment_Mode'].isin(payment)]

# =========================
# TITLE
# =========================
st.title("🍔 Food Delivery Analytics Dashboard")
st.markdown("### Business Insights & Operational Performance")

# =========================
# KPI CALCULATIONS
# =========================

total_orders = len(df)

# Revenue
if 'Final_Amount' in df.columns:
    total_revenue = df['Final_Amount'].sum()
    avg_order_value = df['Final_Amount'].mean()
else:
    total_revenue = 0
    avg_order_value = 0

# Delivery Time
if 'Delivery_Time_Min' in df.columns:
    avg_delivery_time = df['Delivery_Time_Min'].mean()
else:
    avg_delivery_time = 0

# Cancellation Rate
if 'Order_Status' in df.columns:
    cancelled_orders = len(df[df['Order_Status'] == 'Cancelled'])
    cancellation_rate = (cancelled_orders / total_orders) * 100 if total_orders > 0 else 0
else:
    cancellation_rate = 0

# Delivery Rating
if 'Delivery_Rating' in df.columns:
    avg_delivery_rating = df['Delivery_Rating'].mean()
else:
    avg_delivery_rating = 0

# Profit Margin
if 'Profit_Margin_Pct' in df.columns:
    profit_margin = df['Profit_Margin_Pct'].mean()
else:
    profit_margin = 0

# =========================
# KPI CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Total Orders", f"{total_orders:,}")

with col2:
    st.metric("💰 Total Revenue", f"₹ {total_revenue:,.0f}")

with col3:
    st.metric("🛒 Avg Order Value", f"₹ {avg_order_value:.2f}")

with col4:
    st.metric("⏱ Avg Delivery Time", f"{avg_delivery_time:.1f} min")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("❌ Cancellation Rate", f"{cancellation_rate:.2f}%")

with col6:
    st.metric("⭐ Avg Delivery Rating", f"{avg_delivery_rating:.2f}")

with col7:
    st.metric("📈 Profit Margin %", f"{profit_margin:.2f}%")

st.markdown("---")

# =========================
# REVENUE ANALYSIS
# =========================

st.subheader("📊 Revenue & Orders Analysis")

col1, col2 = st.columns(2)

# Revenue by City
if 'City' in df.columns and 'Final_Amount' in df.columns:
    city_revenue = df.groupby('City')['Final_Amount'].sum().reset_index()

    fig_city = px.bar(
        city_revenue,
        x='City',
        y='Final_Amount',
        title='Revenue by City',
        text_auto=True
    )

    col1.plotly_chart(fig_city, use_container_width=True)

# Orders by Cuisine
if 'Cuisine_Type' in df.columns:
    cuisine_orders = df['Cuisine_Type'].value_counts().reset_index()
    cuisine_orders.columns = ['Cuisine_Type', 'Orders']

    fig_cuisine = px.pie(
        cuisine_orders,
        names='Cuisine_Type',
        values='Orders',
        title='Orders by Cuisine Type',
        hole=0.5
    )

    col2.plotly_chart(fig_cuisine, use_container_width=True)

# =========================
# DELIVERY PERFORMANCE
# =========================

st.subheader("🚚 Delivery Performance Analysis")

col3, col4 = st.columns(2)

# Avg Delivery Time by City
if 'City' in df.columns and 'Delivery_Time_Min' in df.columns:
    delivery_city = df.groupby('City')['Delivery_Time_Min'].mean().reset_index()

    fig_delivery = px.bar(
        delivery_city,
        x='City',
        y='Delivery_Time_Min',
        title='Average Delivery Time by City',
        text_auto=True
    )

    col3.plotly_chart(fig_delivery, use_container_width=True)

# Peak Hour Orders
if 'Peak_Hour' in df.columns:
    peak_orders = df['Peak_Hour'].value_counts().reset_index()
    peak_orders.columns = ['Peak_Hour', 'Orders']

    fig_peak = px.bar(
        peak_orders,
        x='Peak_Hour',
        y='Orders',
        title='Peak Hour vs Non-Peak Orders',
        text_auto=True
    )

    col4.plotly_chart(fig_peak, use_container_width=True)

# =========================
# CANCELLATION & RATINGS
# =========================

st.subheader("⭐ Ratings & Cancellation Analysis")

col5, col6 = st.columns(2)

# Cancellation Reasons
if 'Cancellation_Reason' in df.columns:
    cancel_reason = df['Cancellation_Reason'].value_counts().reset_index()
    cancel_reason.columns = ['Reason', 'Count']

    fig_cancel = px.bar(
        cancel_reason,
        x='Reason',
        y='Count',
        title='Cancellation Reasons',
        text_auto=True
    )

    col5.plotly_chart(fig_cancel, use_container_width=True)

# Rating Comparison
if 'Restaurant_Rating' in df.columns and 'Delivery_Rating' in df.columns:
    fig_rating = px.scatter(
        df,
        x='Restaurant_Rating',
        y='Delivery_Rating',
        title='Restaurant Rating vs Delivery Rating',
        opacity=0.7
    )

    col6.plotly_chart(fig_rating, use_container_width=True)

# =========================
# PROFIT ANALYSIS
# =========================

st.subheader("📈 Profitability Analysis")

col7, col8 = st.columns(2)

# Profit Margin by Cuisine
if 'Cuisine_Type' in df.columns and 'Profit_Margin_Pct' in df.columns:
    cuisine_profit = df.groupby('Cuisine_Type')['Profit_Margin_Pct'].mean().reset_index()

    fig_profit = px.bar(
        cuisine_profit,
        x='Cuisine_Type',
        y='Profit_Margin_Pct',
        title='Profit Margin by Cuisine',
        text_auto=True
    )

    col7.plotly_chart(fig_profit, use_container_width=True)

# Revenue vs Profit Margin
if 'Final_Amount' in df.columns and 'Profit_Margin_Pct' in df.columns:
    fig_revenue_profit = px.scatter(
        df,
        x='Final_Amount',
        y='Profit_Margin_Pct',
        title='Revenue vs Profit Margin',
        opacity=0.7
    )

    col8.plotly_chart(fig_revenue_profit, use_container_width=True)

# =========================
# DATA TABLE
# =========================

st.subheader("📋 Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)

# =========================
# FOOTER
# =========================

st.markdown("---")
st.markdown("### 🚀 Built with Streamlit & Plotly")
st.markdown("Food Delivery Business Intelligence Dashboard")
