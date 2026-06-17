# =============================================
# ai_insights.py
# Path: dashboards/streamlit/pages/ai_insights.py
# =============================================

import streamlit as st
import pandas as pd
import json
import os
from db_connection import get_connection

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")
if st.session_state.get("role") == "viewer":
    st.error("🚫 Access denied.")
    st.stop()

st.set_page_config(page_title="AI Insights — Smart Retail", page_icon="🤖", layout="wide")
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
.kpi-value.amber  { color:#f6c90e; }
.kpi-value.red    { color:#ff6b6b; }
.section-title { font-size:1.1rem; font-weight:600; color:#e6edf3;
                 margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #30363d; }
.insight-card { background:rgba(79,172,254,0.07); border:1px solid rgba(79,172,254,0.2);
                border-radius:12px; padding:16px 20px; margin:8px 0;
                color:#e6edf3; font-size:0.92rem; }
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
    if role in ("analyst", "admin"):
        st.page_link("pages/forecasting.py", label="📈 Forecasting")
        st.page_link("pages/ai_insights.py", label="🤖 AI Insights")
    if role == "admin":
        st.page_link("pages/admin.py", label="⚙️ Admin Panel")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

# ---------- PERFORMANCE FIX ----------
# These now read tiny pre-built files (dashboard_summary.json,
# customer_segments.csv, top_states.csv) instead of the full
# 19MB sales_gold.csv every single time. Cache also extended
# from 5 min to 1 hour since this data doesn't change often.

@st.cache_data(ttl=3600)
def load_kpis(gold_path):
    try:
        with open(os.path.join(gold_path, "dashboard_summary.json")) as f:
            summary = json.load(f)
        return (summary["total_revenue"], summary["total_orders"],
                summary["total_customers"], summary["top_state"])
    except Exception:
        try:
            df = pd.read_csv(os.path.join(gold_path, "sales_gold.csv"))
            revenue   = float(df["payment_value"].sum())
            orders    = int(df["order_id"].nunique())
            customers = int(df["customer_id"].nunique())
            top_state = df.groupby("customer_state")["payment_value"].sum().idxmax() \
                        if "customer_state" in df.columns else "N/A"
            return revenue, orders, customers, top_state
        except Exception:
            return 0.0, 0, 0, "N/A"

@st.cache_data(ttl=3600)
def load_top_states(gold_path):
    try:
        df = pd.read_csv(os.path.join(gold_path, "top_states.csv"))
        df.columns = ["State", "Total Revenue", "Total Orders"]
        return df.head(5)
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_customer_segments(gold_path):
    try:
        # Fast path — tiny pre-built file
        return pd.read_csv(os.path.join(gold_path, "customer_segments.csv"))
    except Exception:
        # Fallback — compute from full file (slower, only runs once if needed)
        try:
            df = pd.read_csv(os.path.join(gold_path, "sales_gold.csv"))
            counts = df.groupby("customer_id")["order_id"].nunique().reset_index()
            counts.columns = ["customer_id", "order_count"]
            def seg(n):
                if n >= 5: return "VIP"
                if n >= 2: return "Regular"
                return "New"
            counts["segment"] = counts["order_count"].apply(seg)
            return counts.groupby("segment").size().reset_index(name="customer_count")
        except Exception:
            return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_forecast_growth(gold_path):
    try:
        df = pd.read_csv(os.path.join(gold_path, "sales_forecast.csv"))
        actual_rows   = df[df["sales"]    > 0]
        forecast_rows = df[df["forecast"] > 0]
        if not actual_rows.empty and not forecast_rows.empty:
            last_actual    = actual_rows["sales"].iloc[-1]
            first_forecast = forecast_rows["forecast"].iloc[0]
            return round(((first_forecast - last_actual) / last_actual) * 100, 2) if last_actual > 0 else 0.0
        return 0.0
    except Exception:
        return 0.0

@st.cache_data(ttl=60)  # inventory changes often
def load_low_stock_count():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Inventory WHERE stock_quantity < reorder_level")
        count  = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0

with st.spinner("Loading AI insights..."):
    total_revenue, total_orders, total_customers, top_state = load_kpis(GOLD)
    top_states      = load_top_states(GOLD)
    segments        = load_customer_segments(GOLD)
    forecast_growth = load_forecast_growth(GOLD)
    low_stock_cnt   = load_low_stock_count()

st.markdown("""
<div class="page-title">🤖 AI Business Intelligence</div>
<div class="page-caption">Smart Retail Analytics Platform — Insights, Recommendations & Analytics</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">💰 Total Revenue</div>
        <div class="kpi-value blue">₹{total_revenue:,.0f}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">🏆 Top State</div>
        <div class="kpi-value amber">{top_state}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    colour = "green" if forecast_growth >= 0 else "red"
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">📈 Forecast Growth</div>
        <div class="kpi-value {colour}">{forecast_growth:+.1f}%</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">⚠️ Low Stock</div>
        <div class="kpi-value red">{low_stock_cnt}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-title">🏆 Top 5 Revenue States</div>', unsafe_allow_html=True)
    if not top_states.empty:
        st.dataframe(top_states, use_container_width=True, hide_index=True)
        st.bar_chart(top_states.set_index("State")["Total Revenue"])
    else:
        st.info("No state data available.")

with col2:
    st.markdown('<div class="section-title">👥 Customer Segments</div>', unsafe_allow_html=True)
    if not segments.empty:
        st.dataframe(segments, use_container_width=True, hide_index=True)
        st.bar_chart(segments.set_index("segment")["customer_count"])
    else:
        st.info("No segment data available.")

st.divider()

st.markdown('<div class="section-title">🤖 AI Recommendations</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="insight-card">🏆 <b>Top Revenue State:</b> {top_state} — Focus marketing here for maximum ROI.</div>
<div class="insight-card">📈 <b>Forecast Growth:</b> {forecast_growth:+.1f}% — {"Expand inventory and prepare supply chain." if forecast_growth > 0 else "Review pricing and boost promotions."}</div>
<div class="insight-card">⚠️ <b>Stock Alert:</b> {low_stock_cnt} product(s) below reorder level — Initiate procurement immediately.</div>
<div class="insight-card">💰 <b>Revenue Summary:</b> ₹{total_revenue:,.0f} across {total_orders:,} orders from {total_customers:,} customers.</div>
""", unsafe_allow_html=True)