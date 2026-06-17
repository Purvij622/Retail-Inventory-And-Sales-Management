import streamlit as st
import pandas as pd
import os

# ----------------------------
# AUTH
# ----------------------------
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

with st.sidebar:

    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display:none;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# PATH FIX
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GOLD = os.path.normpath(
    os.path.join(
        BASE_DIR,
        "..",
        "..",
        "..",
        "data",
        "gold"
    )
)

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    

    st.divider()

    st.page_link("pages/dashboard.py", label="📊 Dashboard")
    st.page_link("pages/inventory.py", label="📦 Inventory")

    if st.session_state.role in ("analyst", "admin"):
        st.page_link("pages/forecasting.py", label="📈 Forecasting")
        st.page_link("pages/ai_insights.py", label="🤖 AI Insights")

    st.page_link(
        "pages/customer_segmentation.py",
        label="👥 Customer Segmentation"
    )

    st.page_link(
        "pages/performance_scorecard.py",
        label="🏆 Performance Scorecard"
    )

    st.page_link(
        "pages/universal_analytics.py",
        label="🌍 Universal Analytics"
    )

    if st.session_state.role == "admin":
        st.page_link("pages/admin.py", label="⚙️ Admin Panel")

# ----------------------------
# LOAD DATA
# ----------------------------
try:
    df = pd.read_csv(
        os.path.join(
            GOLD,
            "customer_segments.csv"
        )
    )

except Exception as e:
    st.error(f"❌ Could not load customer_segments.csv\n\n{e}")
    st.stop()

# ----------------------------
# KPIs
# ----------------------------
total_customers = int(df["customer_count"].sum())

vip_customers = 0
regular_customers = 0
new_customers = total_customers

if "VIP" in df["segment"].values:
    vip_customers = int(
        df[df["segment"] == "VIP"]["customer_count"].sum()
    )

if "Regular" in df["segment"].values:
    regular_customers = int(
        df[df["segment"] == "Regular"]["customer_count"].sum()
    )

if "New" in df["segment"].values:
    new_customers = int(
        df[df["segment"] == "New"]["customer_count"].sum()
    )

# ----------------------------
# HEADER
# ----------------------------
st.title("👥 Customer Segmentation")
st.caption(
    "Smart Retail Analytics Platform — Customer Behavior Analysis"
)

st.divider()

# ----------------------------
# KPI CARDS
# ----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with c2:
    st.metric(
        "VIP Customers",
        f"{vip_customers:,}"
    )

with c3:
    st.metric(
        "Regular Customers",
        f"{regular_customers:,}"
    )

with c4:
    st.metric(
        "New Customers",
        f"{new_customers:,}"
    )

st.divider()

# ----------------------------
# SEGMENT TABLE
# ----------------------------
st.subheader("📋 Segment Distribution")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ----------------------------
# CHART
# ----------------------------
st.subheader("📊 Customer Segment Analysis")

st.bar_chart(
    df.set_index("segment")["customer_count"]
)

st.divider()

# ----------------------------
# AI INSIGHTS
# ----------------------------
st.subheader("🤖 AI Insights")

largest_segment = df.loc[
    df["customer_count"].idxmax(),
    "segment"
]

st.success(f"""
Total Customers: {total_customers:,}

Largest Segment: {largest_segment}

Recommendations:

• Improve customer retention strategy

• Launch loyalty rewards program

• Increase repeat purchases

• Create personalized offers

• Build VIP customer programs
""")