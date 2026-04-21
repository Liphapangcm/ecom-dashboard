import streamlit as st
from utils.data_loader import (
    load_data,
    get_revenue_over_time,
    get_top_categories,
    get_revenue_by_state,
    get_weekly_summary_stats,
    get_kpi_summary
)
from components.charts import (
    chart_revenue_over_time,
    chart_top_categories,
    chart_revenue_by_state,
    chart_weekly_trend
)

from components.ai_summary import generate_weekly_summary

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Intelligence Dashboard",
    page_icon="📦",
    layout="wide"
)

# ── Load data (cached so it only runs once) ──────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar filters ──────────────────────────────────────────
st.sidebar.title("📦 Filters")

years = sorted(df["order_year"].unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", options=["All"] + years)

all_categories = sorted(df["product_category_name"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Filter by Category",
    options=all_categories,
    default=[]
)

# Apply filters
filtered_df = df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["order_year"] == selected_year]
if selected_categories:
    filtered_df = filtered_df[filtered_df["product_category_name"].isin(selected_categories)]

# ── Header ───────────────────────────────────────────────────
st.title("E-Commerce Sales Intelligence Dashboard")
st.caption("Brazilian E-Commerce dataset · Olist · 2016–2018")
st.divider()

# ── KPI Row ──────────────────────────────────────────────────
kpis = get_kpi_summary(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"R${kpis['total_revenue']:,.0f}")
col2.metric("📦 Total Orders", f"{kpis['total_orders']:,}")
col3.metric("🧾 Avg Order Value", f"R${kpis['avg_order_value']:,.2f}")
col4.metric("🏆 Top Category", kpis["top_category"].replace("_", " ").title())

st.divider()

# ── Row 1: Revenue trend + Weekly trend ──────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.plotly_chart(
        chart_revenue_over_time(get_revenue_over_time(filtered_df)),
        use_container_width=True
    )

with col_right:
    st.plotly_chart(
        chart_weekly_trend(get_weekly_summary_stats(filtered_df)),
        use_container_width=True
    )

# ── Row 2: Categories + State ─────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.plotly_chart(
        chart_top_categories(get_top_categories(filtered_df)),
        use_container_width=True
    )

with col_right2:
    st.plotly_chart(
        chart_revenue_by_state(get_revenue_by_state(filtered_df)),
        use_container_width=True
    )

# ── AI Summary ────────────────────────────────────────────────
st.divider()
st.subheader("🤖 AI Weekly Summary")

if st.button("Generate AI Summary", type="primary"):
    with st.spinner("Analysing your data..."):
        weekly_data = get_weekly_summary_stats(filtered_df)
        summary = generate_weekly_summary(weekly_data)
        st.success(summary)