# =============================================
# app.py
# =============================================

import streamlit as st

st.set_page_config(
    page_title="Smart Retail Analytics Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
st.markdown("""
<style>

[data-testid="stSidebar"]{
    display:none;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

.stApp{
    background: linear-gradient(
        135deg,
        #0f0c29,
        #302b63,
        #24243e
    );
}

.title{
    text-align:center;
    color:white;
    font-size:60px;
    font-weight:bold;
    margin-top:80px;
}

.subtitle{
    text-align:center;
    color:#d1d5db;
    font-size:22px;
    margin-bottom:60px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------

st.markdown(
    '<div class="title">🛒 Smart Retail Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Enterprise Retail Analytics Platform</div>',
    unsafe_allow_html=True
)

# ----------------------------
# BUTTONS
# ----------------------------

left, login_col, signup_col, right = st.columns([3,1,1,3])

with login_col:
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/login.py")

with signup_col:
    if st.button("📝 Sign Up", use_container_width=True):
        st.switch_page("pages/signup.py")

# ----------------------------
# FOOTER
# ----------------------------

st.markdown("<br><br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align:center;color:#9ca3af;'>
        Built with Python • SQL Server • Power BI
    </div>
    """,
    unsafe_allow_html=True
)