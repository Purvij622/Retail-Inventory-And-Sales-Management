# =============================================
# forecasting.py
# Path: dashboards/streamlit/pages/forecasting.py
# =============================================

import streamlit as st
import pandas as pd
import os
from db_connection import get_connection

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")
if st.session_state.get("role") == "viewer":
    st.error("🚫 Access denied.")
    st.stop()

st.set_page_config(page_title="Forecasting — Smart Retail", page_icon="📈", layout="wide")

st.markdown("""
<style>

/* Hide Streamlit default page navigation */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Hide automatic pages list */
section[data-testid="stSidebar"] ul {
    display: none !important;
}

/* Clean sidebar */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}

</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

GOLD = os.path.join(BASE_DIR, "data", "gold")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0d1117; }
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}

/* Hide Streamlit default page list */
[data-testid="stSidebarNav"] {
    display: none;
}
.page-title   { font-size:1.8rem; font-weight:700; color:#e6edf3; }
.page-caption { color:#8b949e; font-size:0.9rem; }
.kpi-card  { background:#161b22; border:1px solid #30363d; border-radius:14px;
             padding:20px 24px; text-align:center; margin-bottom:8px; }
.kpi-label { font-size:0.8rem; color:#8b949e; font-weight:600;
             text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px; }
.kpi-value        { font-size:1.8rem; font-weight:700; color:#e6edf3; }
.kpi-value.blue   { color:#4facfe; }
.kpi-value.green  { color:#43e97b; }
.kpi-value.red    { color:#ff6b6b; }
.section-title { font-size:1.1rem; font-weight:600; color:#e6edf3;
                 margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div style='padding:16px 0 8px'>
        <div style='font-size:1rem;font-weight:700;color:#e6edf3;'>👤 {st.session_state.user_name}</div>
        <div style='margin-top:8px;'>
            <span style='background:rgba(79,172,254,0.15);color:#4facfe;
                         padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:600;'>
                {st.session_state.role.upper()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("**Navigation**")
    role = st.session_state.role
    st.page_link("pages/dashboard.py",   label="📊 Dashboard")
    st.page_link("pages/inventory.py",   label="📦 Inventory")
    if role in ("analyst", "admin"):
        st.page_link("pages/forecasting.py", label="📈 Forecasting")
        st.page_link("pages/ai_insights.py", label="🤖 AI Insights")

        st.page_link(
    "pages/universal_analytics.py",
    label="🌍 Universal Analytics"
)
        st.page_link(
    "pages/performance_scorecard.py",
    label="🏆 Performance Scorecard"
)
        st.page_link(
    "pages/customer_segmentation.py",
    label="👥 Customer Segmentation"
)
    if role == "admin":
        st.page_link("pages/admin.py", label="⚙️ Admin Panel")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

@st.cache_data(ttl=300)
def load_forecast(gold_path):
    try:
        return pd.read_csv(os.path.join(gold_path, "sales_forecast.csv"))
    except FileNotFoundError:
        return pd.DataFrame()

with st.spinner("Loading forecast..."):
    forecast_df = load_forecast(GOLD)

if forecast_df.empty:
    st.error("❌ Forecast data not found. Run forecasting_pipeline.py first.")
    st.stop()

current_sales  = float(forecast_df[forecast_df["sales"]    > 0]["sales"].sum())
forecast_sales = float(forecast_df[forecast_df["forecast"] > 0]["forecast"].sum())

# Growth % = compare LAST actual month vs FIRST forecast month
# (not total sum, which mixes different time periods)
actual_rows   = forecast_df[forecast_df["sales"]    > 0]
forecast_rows = forecast_df[forecast_df["forecast"] > 0]

if not actual_rows.empty and not forecast_rows.empty:
    last_actual_value  = actual_rows["sales"].iloc[-1]
    first_forecast_value = forecast_rows["forecast"].iloc[0]
    growth = round(((first_forecast_value - last_actual_value) / last_actual_value) * 100, 2) \
             if last_actual_value > 0 else 0
else:
    growth = 0

st.markdown("""
<div class="page-title">📈 Sales Forecasting</div>
<div class="page-caption">AI-Powered 6-Month Sales Forecast Engine</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">💰 Last Month Sales</div>
        <div class="kpi-value blue">₹{last_actual_value:,.0f}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">🚀 Next Month Forecast</div>
        <div class="kpi-value green">₹{first_forecast_value:,.0f}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    colour = "green" if growth >= 0 else "red"
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">📈 Growth %</div>
        <div class="kpi-value {colour}">{growth:+.2f}%</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Sales vs Forecast Trend</div>', unsafe_allow_html=True)
st.line_chart(forecast_df.set_index("year_month")[["sales","forecast"]])

st.divider()
st.markdown('<div class="section-title">📋 Forecast Dataset</div>', unsafe_allow_html=True)
st.dataframe(forecast_df, use_container_width=True, hide_index=True)
csv = forecast_df.to_csv(index=False)
st.download_button("⬇️ Download Forecast CSV", data=csv, file_name="sales_forecast.csv", mime="text/csv")

st.divider()
st.markdown('<div class="section-title">🤖 AI Forecast Analysis</div>', unsafe_allow_html=True)
if growth > 0:
    st.success(f"""**📈 Positive Growth: {growth:+.2f}%**
- Expand inventory to meet forecasted demand
- Scale marketing campaigns
- Review supplier contracts for better pricing""")
else:
    st.warning(f"""**📉 Growth Slowing: {growth:+.2f}%**
- Review pricing strategy
- Increase promotional marketing spend
- Offer seasonal discounts to boost volume""")