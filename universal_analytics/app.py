import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Universal AI Analytics Platform",
    page_icon="🚀",
    layout="wide"
)

# HEADER

st.title("🚀 Universal AI Analytics Platform")
st.caption("Upload Any CSV & Generate Instant Insights")

st.markdown("---")

# FILE UPLOAD

uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    # LOAD DATA

    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset Loaded Successfully")

    st.markdown("---")

    # KPIs

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = df.isnull().sum().sum()

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "📄 Rows",
            total_rows
        )

    with c2:
        st.metric(
            "📊 Columns",
            total_columns
        )

    with c3:
        st.metric(
            "⚠️ Missing Values",
            missing_values
        )

    with c4:
        st.metric(
            "🔢 Numeric Columns",
            len(numeric_cols)
        )

    st.markdown("---")

    # DATA PREVIEW

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.markdown("---")

    # COLUMN INFO

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

    # SUMMARY

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )

    st.markdown("---")

    # AUTO CHARTS

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

    # CORRELATION

    if len(numeric_cols) > 1:

        st.subheader("🔥 Correlation Matrix")

        corr = df[numeric_cols].corr()

        st.dataframe(
            corr,
            use_container_width=True
        )

    st.markdown("---")

    # MISSING VALUES

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

    # AI INSIGHTS

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

    # DOWNLOAD

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