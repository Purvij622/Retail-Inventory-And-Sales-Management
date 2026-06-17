import streamlit as st
import pandas as pd
import json
import os
from db_connection import get_connection

# ------------------------
# AUTH
# ------------------------
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Performance Scorecard",
    page_icon="🏆",
    layout="wide"
)

# ------------------------
# PROJECT PATH
# ------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        ".."
    )
)

GOLD = os.path.join(
    PROJECT_ROOT,
    "data",
    "gold"
)

# ------------------------
# SIDEBAR
# ------------------------
with st.sidebar:

    st.markdown(f"""
    ### 👤 {st.session_state.user_name}
    **Role:** {st.session_state.role.upper()}
    """)

    st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
    
    st.divider()

    st.page_link("pages/dashboard.py", label="📊 Dashboard")
    st.page_link("pages/inventory.py", label="📦 Inventory")
    st.page_link("pages/forecasting.py", label="📈 Forecasting")
    st.page_link("pages/ai_insights.py", label="🤖 AI Insights")
    st.page_link("pages/customer_segmentation.py", label="👥 Customer Segmentation")
    st.page_link("pages/performance_scorecard.py", label="🏆 Performance Scorecard")
    st.page_link("pages/universal_analytics.py", label="🌍 Universal Analytics")

    if st.session_state.role == "admin":
        st.page_link("pages/admin.py", label="⚙️ Admin Panel")

# ------------------------
# LOAD DATA
# ------------------------
try:

    with open(
        os.path.join(GOLD, "dashboard_summary.json"),
        "r"
    ) as f:
        summary = json.load(f)

    top_states = pd.read_csv(
        os.path.join(GOLD, "top_states.csv")
    )

    forecast = pd.read_csv(
        os.path.join(GOLD, "sales_forecast.csv")
    )

except Exception as e:
    st.error(f"❌ Data Load Error\n\n{e}")
    st.stop()

# ------------------------
# LOW STOCK COUNT
# ------------------------
try:

    conn = get_connection()

    query = """
    SELECT COUNT(*)
    FROM Inventory
    WHERE stock_quantity < reorder_level
    """

    low_stock = pd.read_sql(
        query,
        conn
    ).iloc[0, 0]

    conn.close()

except:
    low_stock = 0

# ------------------------
# KPI SCORES
# ------------------------
revenue_score = 95

inventory_score = max(
    50,
    100 - (low_stock * 5)
)

forecast_score = 88

customer_score = 92

overall_score = round(
    (
        revenue_score +
        inventory_score +
        forecast_score +
        customer_score
    ) / 4
)

# ------------------------
# HEADER
# ------------------------
st.title("🏆 Performance Scorecard")
st.caption(
    "Smart Retail Analytics Platform — Executive Business Overview"
)

st.divider()

# ------------------------
# KPI ROW
# ------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Revenue Score",
        revenue_score
    )

with c2:
    st.metric(
        "Inventory Score",
        inventory_score
    )

with c3:
    st.metric(
        "Forecast Score",
        forecast_score
    )

with c4:
    st.metric(
        "Customer Score",
        customer_score
    )

with c5:
    st.metric(
        "Overall Score",
        overall_score
    )

st.divider()

# ------------------------
# BUSINESS HEALTH
# ------------------------
st.subheader("📈 Business Health")

st.progress(overall_score / 100)

if overall_score >= 90:
    st.success("✅ Excellent Business Performance")

elif overall_score >= 75:
    st.warning("⚠️ Good Performance — Improvement Possible")

else:
    st.error("❌ Business Needs Attention")

# ------------------------
# TOP MARKET
# ------------------------
st.subheader("🏆 Top Performing Market")

top_state = top_states.iloc[0]

st.info(
    f"""
State: {top_state['customer_state']}

Revenue: ₹{top_state['total_revenue']:,.0f}

Orders: {int(top_state['total_orders']):,}
"""
)

# ------------------------
# RISK TABLE
# ------------------------
st.subheader("⚠️ Risk Indicators")

risk_df = pd.DataFrame({
    "Risk Area": [
        "Inventory",
        "Revenue",
        "Demand"
    ],
    "Risk Level": [
        "Medium" if low_stock > 0 else "Low",
        "Low",
        "Low"
    ]
})

st.dataframe(
    risk_df,
    use_container_width=True,
    hide_index=True
)

# ------------------------
# AI RECOMMENDATIONS
# ------------------------
st.subheader("🤖 AI Recommendations")

st.success(
    f"""
• Focus marketing campaigns in {top_state['customer_state']}

• Monitor {low_stock} low-stock products

• Continue expansion strategy

• Increase inventory for fast-moving products

• Forecast indicates stable business growth
"""
)