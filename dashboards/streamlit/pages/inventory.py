# =============================================
# inventory.py
# Path: dashboards/streamlit/pages/inventory.py
# =============================================

import streamlit as st
import pandas as pd
from db_connection import get_connection

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Inventory — Smart Retail",
    page_icon="📦",
    layout="wide"
)
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
.kpi-value       { font-size:1.8rem; font-weight:700; color:#e6edf3; }
.kpi-value.blue  { color:#4facfe; }
.kpi-value.green { color:#43e97b; }
.kpi-value.red   { color:#ff6b6b; }
.section-title   { font-size:1.1rem; font-weight:600; color:#e6edf3;
                   margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
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
        st.page_link("pages/admin.py",       label="⚙️ Admin Panel")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

# ---------- Load Inventory from SQL ----------
@st.cache_data(ttl=60)
def load_inventory():
    try:
        conn = get_connection()
        df = pd.read_sql("""
            SELECT
                inventory_id,
                product_id,
                product_name,
                stock_quantity,
                reorder_level,
                unit_price,
                CASE
                    WHEN stock_quantity = 0             THEN 'Out of Stock'
                    WHEN stock_quantity < reorder_level THEN 'Low Stock'
                    ELSE 'In Stock'
                END AS status
            FROM Inventory
            ORDER BY stock_quantity ASC
        """, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Could not load inventory: {e}")
        return pd.DataFrame()

inventory_df = load_inventory()

# ---------- KPIs ----------
total_products  = len(inventory_df)
low_stock_count = len(inventory_df[inventory_df["status"] == "Low Stock"])  if not inventory_df.empty else 0
out_of_stock    = len(inventory_df[inventory_df["status"] == "Out of Stock"]) if not inventory_df.empty else 0
total_value     = float((inventory_df["stock_quantity"] * inventory_df["unit_price"]).sum()) if not inventory_df.empty else 0

# ---------- Header ----------
st.markdown("""
<div class="page-title">📦 Inventory Management</div>
<div class="page-caption">Smart Retail — Stock Overview & Management</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------- KPI Row ----------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total Products</div>
        <div class="kpi-value blue">{total_products}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Low Stock</div>
        <div class="kpi-value red">{low_stock_count}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Out of Stock</div>
        <div class="kpi-value red">{out_of_stock}</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Inventory Value</div>
        <div class="kpi-value green">₹{total_value:,.0f}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Add Product (Admin/Analyst only) ----------
role = st.session_state.role

if role in ("admin", "analyst"):
    st.markdown('<div class="section-title">➕ Add New Product</div>', unsafe_allow_html=True)

    with st.form("add_product_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            product_id   = st.text_input("Product ID",   placeholder="e.g. P006")
            product_name = st.text_input("Product Name", placeholder="e.g. USB Hub")
        with col2:
            stock   = st.number_input("Stock Quantity", min_value=0, value=0)
            reorder = st.number_input("Reorder Level",  min_value=0, value=10)
        unit_price = st.number_input("Unit Price (₹)", min_value=0.0, value=0.0, step=10.0)
        submitted  = st.form_submit_button("➕ Add Product", use_container_width=True)

    if submitted:
        if not product_id or not product_name:
            st.error("⚠️ Product ID and Name are required.")
        else:
            try:
                conn   = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Inventory
                        (product_id, product_name, stock_quantity, reorder_level, unit_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_id, product_name, stock, reorder, unit_price))
                conn.commit()
                conn.close()
                st.success(f"✅ '{product_name}' added to inventory.")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

# ---------- Inventory Table ----------
st.markdown('<div class="section-title">📋 Current Inventory</div>', unsafe_allow_html=True)

if not inventory_df.empty:
    def colour_status(val):
        if val == "Low Stock":
            return "background-color: rgba(255,107,107,0.15); color: #ff6b6b;"
        elif val == "Out of Stock":
            return "background-color: rgba(255,60,60,0.25); color: #ff4444;"
        return "background-color: rgba(67,233,123,0.1); color: #43e97b;"

    styled = inventory_df.style.map(colour_status, subset=["status"])
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="section-title">📊 Stock Level Overview</div>', unsafe_allow_html=True)
    chart_df = inventory_df.set_index("product_name")[["stock_quantity", "reorder_level"]]
    st.bar_chart(chart_df)
else:
    st.info("No inventory data found.")

st.divider()

# ---------- AI Insights ----------
st.markdown('<div class="section-title">🤖 Inventory Insights</div>', unsafe_allow_html=True)
if not inventory_df.empty:
    low_items = inventory_df[inventory_df["status"].isin(["Low Stock","Out of Stock"])]["product_name"].tolist()
    # Convert any NaN/None/float values to string "Unknown Product"
    low_items = [str(item) if pd.notna(item) else "Unknown Product" for item in low_items]
    if low_items:
        st.warning(f"""
        ⚠️ **{len(low_items)} product(s) need attention:** {', '.join(low_items)}

        **Recommended Actions:**
        - Reorder low stock items immediately
        - Increase reorder levels for fast-moving products
        - Review supplier lead times
        """)
    else:
        st.success("✅ All products are well stocked. No action needed.")