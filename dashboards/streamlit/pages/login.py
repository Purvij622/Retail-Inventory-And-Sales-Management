# =============================================
# Login.py
# Path: dashboards/streamlit/pages/Login.py
# =============================================

import streamlit as st
import bcrypt
import re
from db_connection import get_connection

st.set_page_config(
    page_title="Login — Smart Retail",
    page_icon="🔐",
    layout="centered"
)

# ---------- CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

.login-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 40px 36px;
    margin-top: 20px;
}

.login-title {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    margin-bottom: 4px;
}

.login-sub {
    color: #a0aec0;
    text-align: center;
    font-size: 0.95rem;
    margin-bottom: 28px;
}

label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}

input:focus {
    border-color: #4facfe !important;
    box-shadow: 0 0 0 2px rgba(79,172,254,0.25) !important;
}

.stButton > button {
    width: 100%;
    height: 52px;
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    color: #0f0c29;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
}

.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

.back-link {
    text-align: center;
    color: #718096;
    font-size: 0.85rem;
    margin-top: 16px;
}

/* Email valid/invalid hint */
.hint-valid   { color: #43e97b; font-size: 0.8rem; margin-top: -8px; }
.hint-invalid { color: #ff6b6b; font-size: 0.8rem; margin-top: -8px; }

</style>
""", unsafe_allow_html=True)

# ---------- Redirect if already logged in ----------
if st.session_state.get("logged_in"):
    st.switch_page("pages/dashboard.py")

# ---------- Email validation helper ----------
def is_valid_email(email):
    # Simple regex: something@something.something
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

# ---------- UI ----------
st.markdown("""
<div class="login-card">
    <div class="login-title">🔐 Welcome Back</div>
    <div class="login-sub">Sign in to your Smart Retail account</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

email    = st.text_input("📧 Email Address", placeholder="you@example.com")
password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

# ---------- Live email format hint ----------
# Shows green tick or red cross as user types
if email:
    if is_valid_email(email):
        st.markdown('<p class="hint-valid">✅ Valid email format</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="hint-invalid">❌ Invalid email format (e.g. name@example.com)</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔐 Login"):

    # Check empty fields
    if not email or not password:
        st.error("⚠️ Please fill in all fields.")

    # Check email format before hitting DB
    elif not is_valid_email(email):
        st.error("❌ Please enter a valid email address.")

    else:
        # Loading spinner while checking credentials
        with st.spinner("🔄 Verifying credentials..."):
            try:
                conn   = get_connection()
                cursor = conn.cursor()

                # Fetch user by email only
                cursor.execute(
                    "SELECT user_id, full_name, email, password, role FROM Users WHERE email = ?",
                    (email,)
                )
                user = cursor.fetchone()
                conn.close()

                if user is None:
                    st.error("❌ No account found with this email.")

                else:
                    # bcrypt compare: typed password vs stored hash
                    password_correct = bcrypt.checkpw(
                        password.encode("utf-8"),
                        user[3].encode("utf-8")
                    )

                    if password_correct:
                        # Store in session
                        st.session_state.logged_in  = True
                        st.session_state.user_id    = user[0]
                        st.session_state.user_name  = user[1]
                        st.session_state.user_email = user[2]
                        st.session_state.role       = user[4]

                        st.success(f"✅ Welcome back, {user[1]}!")
                        st.switch_page("pages/dashboard.py")

                    else:
                        st.error("❌ Incorrect password. Please try again.")

            except Exception as e:
                st.error(f"❌ Login error: {e}")

# Back link
st.markdown("<br>", unsafe_allow_html=True)
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("""
<div class="back-link">
    Don't have an account? Use the Sign Up page.
</div>
""", unsafe_allow_html=True)