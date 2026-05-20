import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Food Delivery Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PROFESSIONAL DARK UI CSS
# =========================================================

st.markdown("""
<style>

/* ===== GLOBAL ===== */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f172a;
    color: #f8fafc;
}

/* App Background */

[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 100%
    );
}

/* Main Area */

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Titles */

h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -1px;
}

h2 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
}

/* KPI Cards */

```css
[data-testid="metric-container"] {
    background: rgba(17,24,39,0.75) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    padding: 0.9rem 1rem !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    transition: all 0.25s ease;
    backdrop-filter: blur(10px);
    min-height: 140px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 12px 30px rgba(59,130,246,0.18);
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    overflow-wrap: break-word !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #22c55e !important;
    font-weight: 700 !important;
}

/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 10px 18px;
    color: #cbd5e1;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: #2563eb !important;
    color: white !important;
}

/* Chart Containers */

.chart-container {
    background: rgba(17,24,39,0.75);
    border-radius: 18px;
    padding: 1rem;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
}

/* Labels */

label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* Dataframe */

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* Expander */

.streamlit-expanderHeader {
    color: white !important;
    font-weight: 700 !important;
}

/* Scrollbar */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data(show_spinner=False)
def load_data():

    df = pd.read_csv("Final_dataset.csv")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Remove duplicate rows
    df = df.drop_duplicates()

    return df


# Load Data
df = load_data()

# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([0.8, 0.2])

with col1:

    st.markdown("# 🍽️ Food Delivery Analytics Dashboard")

    st.markdown("""
    <div style='color:#94a3b8;font-size:16px;font-weight:500'>
    Real-Time Business Intelligence & Performance Monitoring
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div style='
        text-align:right;
        color:#94a3b8;
        padding-top:18px;
        font-size:14px;
        font-weight:600'>
        🕒 {datetime.now().strftime('%d %b %Y | %H:%M')}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🔍 Dashboard Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [
        df['order_date'].min().date(),
        df['order_date'].max().date()
    ]
)

selected_cities = st.sidebar.multiselect(
    "Cities",
    options=sorted(df['city'].unique()),
    default=sorted(df['city'].unique())[:5]
)

selected_cuisines = st.sidebar.multiselect(
    "Cuisines",
    options=sorted(df['cuisine_type'].unique()),
    default=sorted(df['cuisine_type'].unique())[:5]
)

selected_status = st.sidebar.multiselect(
    "Order Status",
    options=df['order_status'].unique(),
    default=df['order_status'].unique()
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df['order_date'].dt.date >= date_range[0]) &
    (df['order_date'].dt.date <= date_range[1]) &
    (df['city'].isin(selected_cities)) &
    (df['cuisine_type'].isin(selected_cuisines)) &
    (df['order_status'].isin(selected_status))
].copy()
# Remove unrealistic order values


# =========================================================
# NORMALIZE UNREALISTIC ORDER VALUES
# =========================================================

# Scale down unrealistic food order amounts

filtered_df['order_value'] = (
    filtered_df['order_value'] * 0.25
)

filtered_df['final_amount'] = (
    filtered_df['final_amount'] * 0.25
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_orders = len(filtered_df)

total_revenue = filtered_df['final_amount'].sum()

avg_order_value = filtered_df['order_value'].mean()

avg_delivery_time = filtered_df['delivery_time_min'].mean()

cancelled_orders = len(
    filtered_df[
        filtered_df['order_status'] == 'Cancelled'
    ]
)

cancellation_rate = (
    cancelled_orders / total_orders * 100
) if total_orders > 0 else 0

avg_delivery_rating = filtered_df['delivery_rating'].mean()

profit_margin_pct = filtered_df['profit_margin_pct'].mean()


# =========================================================
# KPI SECTION
# =========================================================

st.markdown("## 📊 Key Performance Indicators")

row1 = st.columns(4)

row2 = st.columns(3)

with row1[0]:
    st.metric(
        "Total Orders",
        f"{total_orders:,}",
        "Processed"
    )

with row1[1]:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue/10000000:.1f} Cr"
    )

with row1[2]:
    st.metric(
        "Avg Order Value",
        f"₹{avg_order_value:,.0f}",
        "Per Order"
    )

with row1[3]:
    st.metric(
        "Avg Delivery Time",
        f"{avg_delivery_time:.1f} min",
        "Delivery Speed"
    )

with row2[0]:
    st.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%",
        f"{cancelled_orders} Orders"
    )

with row2[1]:
    st.metric(
        "Delivery Rating",
        f"{avg_delivery_rating:.2f}/5",
        "Customer Rating"
    )

with row2[2]:
    st.metric(
        "Profit Margin",
        f"{profit_margin_pct:.2f}%",
        "Business Margin"
    )

st.markdown("<div style='margin-top:25px'></div>", unsafe_allow_html=True)

# =========================================================
# MAP VISUALIZATION
# =========================================================

st.markdown("## 🌍 Geographic Delivery Insights")

city_map = filtered_df.groupby('city').agg({
    'final_amount': 'sum',
    'distance_km': 'mean'
}).reset_index()

city_coords = {
    "Mumbai": [19.0760, 72.8777],
    "Delhi": [28.7041, 77.1025],
    "Bangalore": [12.9716, 77.5946],
    "Chennai": [13.0827, 80.2707],
    "Hyderabad": [17.3850, 78.4867]
}

city_map['lat'] = city_map['city'].map(
    lambda x: city_coords.get(x, [0,0])[0]
)

city_map['lon'] = city_map['city'].map(
    lambda x: city_coords.get(x, [0,0])[1]
)

st.map(city_map[['lat', 'lon']])

st.markdown("<div style='margin-top:25px'></div>", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================

tab2, tab3, tab4, tab5 = st.tabs([
    "❌ Cancellations",
    "🚗 Delivery",
    "⭐ Ratings",
    "🏆 Top Performers"
])

# =========================================================
# TAB 2
# =========================================================

with tab2:

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        status_counts = filtered_df[
            'order_status'
        ].value_counts()

        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            hole=0.5,
            template='plotly_dark'
        )

        fig.update_layout(
            title='Order Status Distribution',
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        cancelled_df = filtered_df[
            filtered_df['order_status'] == 'Cancelled'
        ]

        if len(cancelled_df) > 0:

            reasons = cancelled_df[
                'cancellation_reason'
            ].value_counts().head(10)

            fig = px.bar(
                reasons,
                orientation='h',
                template='plotly_dark'
            )

            fig.update_layout(
                title='Cancellation Reasons',
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TAB 3
# =========================================================

with tab3:

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        fig = px.histogram(
            filtered_df,
            x='delivery_time_min',
            nbins=30,
            template='plotly_dark'
        )

        fig.update_layout(
            title='Delivery Time Distribution',
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        performance = filtered_df.groupby(
            'delivery_performance'
        )['delivery_rating'].mean()

        fig = px.bar(
            performance,
            template='plotly_dark'
        )

        fig.update_layout(
            title='Performance vs Ratings',
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TAB 4
# =========================================================

with tab4:

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        fig = px.histogram(
            filtered_df,
            x='delivery_rating',
            nbins=5,
            template='plotly_dark'
        )

        fig.update_layout(
            title='Delivery Rating Distribution',
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        fig = px.histogram(
            filtered_df,
            x='restaurant_rating',
            nbins=10,
            template='plotly_dark'
        )

        fig.update_layout(
            title='Restaurant Rating Distribution',
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TAB 5
# =========================================================

with tab5:

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        top_restaurants = filtered_df.groupby(
            'restaurant_name'
        )['final_amount'].sum().sort_values(
            ascending=True
        ).tail(10)

        fig = px.bar(
            top_restaurants,
            orientation='h',
            template='plotly_dark'
        )

        fig.update_layout(
            title='Top Restaurants by Revenue',
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        cuisine = filtered_df[
            'cuisine_type'
        ].value_counts().head(10)

        fig = px.bar(
            cuisine,
            template='plotly_dark'
        )

        fig.update_layout(
            title='Top Ordered Cuisines',
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# RAW DATA
# =========================================================

with st.expander("📋 View Detailed Dataset"):

    st.dataframe(
        filtered_df.head(500),
        use_container_width=True,
        height=400
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)

st.success(
    f"Dashboard Active • {total_orders:,} Orders Loaded • Updated Successfully"
)