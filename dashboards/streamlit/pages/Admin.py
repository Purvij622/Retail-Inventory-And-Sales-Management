# =============================================
# admin.py  ← NEW FILE
# Path: dashboards/streamlit/pages/admin.py
# =============================================

import streamlit as st
import pandas as pd
from db_connection import get_connection

# ---------- Auth Guard ----------
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

# Only admin can access this page
if st.session_state.get("role") != "admin":
    st.error("🚫 Access Denied. Admin only.")
    st.stop()

st.set_page_config(
    page_title="Admin Panel — Smart Retail",
    page_icon="⚙️",
    layout="wide"
)

# ---------- CSS ----------
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
.section-title { font-size:1.1rem; font-weight:600; color:#e6edf3;
                 margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #30363d; }
.kpi-card  { background:#161b22; border:1px solid #30363d; border-radius:14px;
             padding:20px 24px; text-align:center; }
.kpi-label { font-size:0.8rem; color:#8b949e; font-weight:600; text-transform:uppercase;
             letter-spacing:0.05em; margin-bottom:8px; }
.kpi-value { font-size:1.8rem; font-weight:700; color:#4facfe; }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(f"""
    <div style='padding:16px 0 8px'>
        <div style='font-size:1rem;font-weight:700;color:#e6edf3;'>
            👤 {st.session_state.user_name}
        </div>
        <div style='margin-top:8px;'>
            <span style='background:rgba(79,172,254,0.15);color:#4facfe;
                         padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:600;'>
                ADMIN
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("**Navigation**")
    st.page_link("pages/dashboard.py",   label="📊 Dashboard")
    st.page_link("pages/inventory.py",   label="📦 Inventory")
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
    st.page_link("pages/admin.py",       label="⚙️ Admin Panel")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

# ---------- Load Users ----------
def load_users():
    conn = get_connection()
    df = pd.read_sql(
        "SELECT user_id, full_name, email, role FROM Users ORDER BY user_id",
        conn
    )
    conn.close()
    return df

users_df = load_users()

# ---------- Header ----------
st.markdown("""
<div class="page-title">⚙️ Admin Panel</div>
<div class="page-caption">Manage users and system settings</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------- KPI ----------
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total Users</div>
        <div class="kpi-value">{len(users_df)}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    admins = len(users_df[users_df["role"] == "admin"])
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Admins</div>
        <div class="kpi-value">{admins}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    analysts = len(users_df[users_df["role"] == "analyst"])
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Analysts</div>
        <div class="kpi-value">{analysts}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- All Users Table ----------
st.markdown('<div class="section-title">👥 All Users</div>', unsafe_allow_html=True)
st.dataframe(users_df, use_container_width=True, hide_index=True)

st.divider()

# ---------- Update Role ----------
st.markdown('<div class="section-title">🔧 Update User Role</div>', unsafe_allow_html=True)

with st.form("update_role_form"):
    user_email = st.selectbox("Select User", users_df["email"].tolist())
    new_role   = st.selectbox("New Role", ["admin", "analyst", "viewer"])
    submitted  = st.form_submit_button("✅ Update Role", use_container_width=True)

if submitted:
    # Prevent admin from downgrading their own account
    if user_email == st.session_state.user_email and new_role != "admin":
        st.error("⚠️ You cannot change your own admin role.")
    else:
        try:
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Users SET role = ? WHERE email = ?",
                (new_role, user_email)
            )
            conn.commit()
            conn.close()
            st.success(f"✅ Role updated to '{new_role}' for {user_email}")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.divider()

# ---------- Delete User ----------
st.markdown('<div class="section-title">🗑️ Delete User</div>', unsafe_allow_html=True)

# Don't show current admin in delete list
deletable = users_df[users_df["email"] != st.session_state.user_email]["email"].tolist()

with st.form("delete_user_form"):
    del_email  = st.selectbox("Select User to Delete", deletable)
    confirm    = st.checkbox("I confirm I want to delete this user")
    del_submit = st.form_submit_button("🗑️ Delete User", use_container_width=True)

if del_submit:
    if not confirm:
        st.warning("⚠️ Please check the confirmation box.")
    else:
        try:
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Users WHERE email = ?", (del_email,))
            conn.commit()
            conn.close()
            st.success(f"✅ User '{del_email}' deleted.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")