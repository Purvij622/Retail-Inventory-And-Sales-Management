import streamlit as st
import pandas as pd
import numpy as np

# ---------------- AUTH ----------------

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Universal Analytics",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>

/* Hide Streamlit default page navigator */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Hide automatic pages list */
section[data-testid="stSidebar"] ul {
    display: none !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown(f"""
    ### 👤 {st.session_state.user_name}
    **Role:** {st.session_state.role.upper()}
    """)

    st.divider()

    st.markdown("### Navigation")

    role = st.session_state.role

    st.page_link(
        "pages/dashboard.py",
        label="📊 Dashboard"
    )

    st.page_link(
        "pages/inventory.py",
        label="📦 Inventory"
    )

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

        st.page_link(
            "pages/forecasting.py",
            label="📈 Forecasting"
        )

        st.page_link(
            "pages/ai_insights.py",
            label="🤖 AI Insights"
        )

    if role == "admin":

        st.page_link(
            "pages/admin.py",
            label="⚙️ Admin Panel"
        )

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")


# ---------------- PAGE ----------------

st.title("🚀 Universal AI Analytics Platform")
st.caption("Upload Any CSV & Generate Instant Insights")

st.markdown("---")

uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset Loaded Successfully")

    st.markdown("---")

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = df.isnull().sum().sum()

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📄 Rows", total_rows)

    with c2:
        st.metric("📊 Columns", total_columns)

    with c3:
        st.metric("⚠️ Missing Values", missing_values)

    with c4:
        st.metric("🔢 Numeric Columns", len(numeric_cols))

    st.markdown("---")

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🧾 Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(
        info_df,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )

    st.markdown("---")

    if len(numeric_cols) > 0:

        st.subheader("📊 Numeric Trends")

        selected_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        st.line_chart(
            df[selected_col]
        )

        st.bar_chart(
            df[selected_col]
        )

    st.markdown("---")

    if len(numeric_cols) > 1:

        st.subheader("🔥 Correlation Matrix")

        corr = df[numeric_cols].corr()

        st.dataframe(
            corr,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("⚠️ Missing Values Analysis")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum()
    })

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🤖 AI Insights")

    highest_missing = (
        missing_df.sort_values(
            by="Missing Values",
            ascending=False
        )
        .iloc[0]
    )

    st.success(f"""
Dataset contains {total_rows} rows and {total_columns} columns.

Numeric columns detected: {len(numeric_cols)}

Column with highest missing values:
{highest_missing['Column']}

Dataset successfully processed.

Ready for advanced analytics.
""")

    st.markdown("---")

    st.download_button(
        "⬇️ Download Dataset",
        data=df.to_csv(index=False),
        file_name="processed_dataset.csv",
        mime="text/csv"
    )

else:

    st.info(
        "📂 Upload a CSV file to begin analysis."
    )