# =============================================
# dashboard.py
# Path: dashboards/streamlit/pages/dashboard.py
# =============================================

import streamlit as st
import pandas as pd
import json
import os
from db_connection import get_connection

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Dashboard — Smart Retail",
    page_icon="📊",
    layout="wide"
)

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
.kpi-card:hover { border-color:#4facfe; }
.kpi-label { font-size:0.8rem; color:#8b949e; font-weight:600;
             text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px; }
.kpi-value        { font-size:1.8rem; font-weight:700; color:#e6edf3; }
.kpi-value.blue   { color:#4facfe; }
.kpi-value.green  { color:#43e97b; }
.kpi-value.amber  { color:#f6c90e; }
.section-title    { font-size:1.1rem; font-weight:600; color:#e6edf3;
                    margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #30363d; }
.alert-low { background:rgba(255,107,107,0.1); border:1px solid rgba(255,107,107,0.3);
             border-radius:10px; padding:10px 16px; color:#ff6b6b;
             font-size:0.9rem; margin:4px 0; }
</style>
""", unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:16px 0 8px'>
            <div style='font-size:1rem;font-weight:700;color:#e6edf3;'>
                👤 {st.session_state.user_name}
            </div>
            <div style='font-size:0.8rem;color:#8b949e;margin-top:4px;'>
                {st.session_state.user_email}
            </div>
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

render_sidebar()

# ---------- PERFORMANCE FIX ----------
# Instead of reading the full 19MB sales_gold.csv every time,
# read a tiny pre-calculated JSON summary file (few KB).
# This makes the dashboard load almost instantly.
# Run notebooks/build_summary.py once to generate this file.
@st.cache_data(ttl=3600)  # cache for 1 hour, not 5 min — fewer reloads
def load_kpis(gold_path):
    try:
        with open(os.path.join(gold_path, "dashboard_summary.json")) as f:
            summary = json.load(f)
        return summary["total_revenue"], summary["total_orders"], summary["total_customers"]
    except Exception:
        # Fallback: if summary file doesn't exist yet, read full CSV (slower)
        try:
            df        = pd.read_csv(os.path.join(gold_path, "sales_gold.csv"))
            revenue   = float(df["payment_value"].sum())
            orders    = int(df["order_id"].nunique())
            customers = int(df["customer_id"].nunique())
            return revenue, orders, customers
        except Exception:
            return 0.0, 0, 0

@st.cache_data(ttl=3600)
def load_monthly(gold_path):
    try:
        return pd.read_csv(os.path.join(gold_path, "monthly_sales_trend.csv"))
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=60)  # inventory changes often, so shorter cache
def load_low_stock():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_name, stock_quantity, reorder_level
            FROM Inventory WHERE stock_quantity < reorder_level
        """)
        rows = cursor.fetchall()
        conn.close()
        return pd.DataFrame(rows, columns=["product_name","stock_quantity","reorder_level"])
    except Exception:
        return pd.DataFrame()

with st.spinner("Loading dashboard..."):
    total_revenue, total_orders, total_customers = load_kpis(GOLD)
    monthly_df = load_monthly(GOLD)
    low_stock  = load_low_stock()

avg_order = round(total_revenue / total_orders, 2) if total_orders > 0 else 0

st.markdown("""
<div class="page-title">📊 Executive Dashboard</div>
<div class="page-caption">Smart Retail Analytics Platform — Real-time Business Overview</div>
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
        <div class="kpi-label">📦 Total Orders</div>
        <div class="kpi-value green">{total_orders:,}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">👥 Customers</div>
        <div class="kpi-value amber">{total_customers:,}</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">🛒 Avg Order Value</div>
        <div class="kpi-value">₹{avg_order:,}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="section-title">📈 Monthly Revenue Trend</div>', unsafe_allow_html=True)
    if not monthly_df.empty:
        chart_col = "monthly_revenue" if "monthly_revenue" in monthly_df.columns else monthly_df.columns[-1]
        idx_col   = "year_month"      if "year_month"      in monthly_df.columns else monthly_df.columns[0]
        st.line_chart(monthly_df.set_index(idx_col)[chart_col])
    else:
        st.info("No monthly data available yet.")
with col2:
    st.markdown('<div class="section-title">📋 Monthly Data</div>', unsafe_allow_html=True)
    st.dataframe(monthly_df, use_container_width=True, height=280)

st.divider()

st.markdown('<div class="section-title">⚠️ Low Stock Alerts</div>', unsafe_allow_html=True)
if not low_stock.empty:
    for _, row in low_stock.iterrows():
        name = row.get("product_name", "Unknown")
        st.markdown(f"""
        <div class="alert-low">
            ⚠️ <b>{name}</b> — Stock: {row['stock_quantity']} (Reorder at: {row['reorder_level']})
        </div>""", unsafe_allow_html=True)
else:
    st.success("✅ All products are well stocked.")

st.divider()

st.markdown('<div class="section-title">📥 Export Data</div>', unsafe_allow_html=True)
if not monthly_df.empty:
    csv = monthly_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Monthly Revenue CSV",
        data=csv,
        file_name="monthly_revenue.csv",
        mime="text/csv"
    )