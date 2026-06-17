# =============================================
# Signup.py
# Path: dashboards/streamlit/pages/Signup.py
# =============================================

import streamlit as st
import bcrypt
import re
from db_connection import get_connection

st.set_page_config(
    page_title="Sign Up — Smart Retail",
    page_icon="📝",
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

.signup-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 40px 36px;
    margin-top: 20px;
}

.signup-title {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    margin-bottom: 4px;
}

.signup-sub {
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

input, select {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}

input:focus {
    border-color: #4facfe !important;
    box-shadow: 0 0 0 2px rgba(79,172,254,0.25) !important;
}

.role-info {
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 10px;
    padding: 12px 16px;
    margin: 12px 0;
    font-size: 0.83rem;
    color: #90cdf4;
}

/* Password strength bar */
.strength-wrap  { margin: 4px 0 12px; }
.strength-label { font-size:0.8rem; font-weight:600; margin-bottom:4px; }
.strength-bar   { height:6px; border-radius:4px; transition: width 0.3s; }

.hint-valid   { color: #43e97b; font-size: 0.8rem; }
.hint-invalid { color: #ff6b6b; font-size: 0.8rem; }

.stButton > button {
    width: 100%;
    height: 52px;
    background: linear-gradient(90deg, #43e97b, #38f9d7);
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
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def is_valid_email(email):
    """Check email format using regex"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def password_strength(password):
    """
    Returns (score 0-4, label, colour)
    Checks: length, uppercase, digit, special char
    """
    score = 0
    if len(password) >= 6:  score += 1
    if len(password) >= 10: score += 1
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'[0-9]', password): score += 1
    if re.search(r'[^A-Za-z0-9]', password): score += 1

    if score <= 1: return score, "Weak",   "#ff6b6b"
    if score <= 2: return score, "Fair",   "#f6c90e"
    if score <= 3: return score, "Good",   "#4facfe"
    return score,  "Strong", "#43e97b"

# ---------- UI ----------
st.markdown("""
<div class="signup-card">
    <div class="signup-title">📝 Create Account</div>
    <div class="signup-sub">Join the Smart Retail Analytics Platform</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Form ----------
with st.form("signup_form", clear_on_submit=True):

    full_name = st.text_input("👤 Full Name", placeholder="John Doe")
    email     = st.text_input("📧 Email Address", placeholder="you@example.com")

    col1, col2 = st.columns(2)
    with col1:
        password = st.text_input("🔒 Password", type="password", placeholder="Min 6 characters")
    with col2:
        confirm  = st.text_input("🔒 Confirm Password", type="password", placeholder="Repeat password")

    role = st.selectbox(
        "🎯 Select Role",
        ["analyst", "viewer", "admin"],
        help="analyst = full access | viewer = read only | admin = manage users"
    )

    role_desc = {
        "admin":   "⚙️ Admin — full access including user management",
        "analyst": "📊 Analyst — access to dashboards, forecasting & AI insights",
        "viewer":  "👁️ Viewer — read-only access to main dashboard"
    }
    st.markdown(f'<div class="role-info">{role_desc[role]}</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("🚀 Create Account")

# ---------- Live Hints (outside form — updates as user types) ----------
# Email hint
if email:
    if is_valid_email(email):
        st.markdown('<p class="hint-valid">✅ Valid email format</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="hint-invalid">❌ Invalid email — use format: name@example.com</p>', unsafe_allow_html=True)

# Password strength meter
if password:
    score, label, colour = password_strength(password)
    bar_width = min(score * 20, 100)  # 0-100%
    st.markdown(f"""
    <div class="strength-wrap">
        <div class="strength-label" style="color:{colour};">
            Password Strength: {label}
        </div>
        <div style="background:#30363d; border-radius:4px; height:6px;">
            <div class="strength-bar"
                 style="width:{bar_width}%; background:{colour}; height:6px; border-radius:4px;">
            </div>
        </div>
        <div style="color:#8b949e; font-size:0.75rem; margin-top:4px;">
            Tips: Use uppercase, numbers & special characters (!@#$)
        </div>
    </div>
    """, unsafe_allow_html=True)

# Password match hint
if password and confirm:
    if password == confirm:
        st.markdown('<p class="hint-valid">✅ Passwords match</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="hint-invalid">❌ Passwords do not match</p>', unsafe_allow_html=True)

# ---------- Handle Submit ----------
if submitted:

    # 1. Empty field check
    if not full_name or not email or not password or not confirm:
        st.error("⚠️ Please fill in all fields.")

    # 2. Email format check
    elif not is_valid_email(email):
        st.error("❌ Please enter a valid email address (e.g. name@example.com)")

    # 3. Full name — only letters and spaces
    elif not re.match(r'^[A-Za-z\s]{2,}$', full_name.strip()):
        st.error("❌ Full name should contain only letters and spaces (min 2 characters).")

    # 4. Password length
    elif len(password) < 6:
        st.error("⚠️ Password must be at least 6 characters.")

    # 5. Passwords match
    elif password != confirm:
        st.error("❌ Passwords do not match.")

    else:
        # Loading spinner while saving to DB
        with st.spinner("🔄 Creating your account..."):
            try:
                conn   = get_connection()
                cursor = conn.cursor()

                # Check duplicate email
                cursor.execute("SELECT email FROM Users WHERE email = ?", (email,))
                existing = cursor.fetchone()

                if existing:
                    st.error("❌ This email is already registered. Please login.")

                else:
                    # Hash password with bcrypt
                    hashed_password = bcrypt.hashpw(
                        password.encode("utf-8"),
                        bcrypt.gensalt()
                    )

                    # Save to DB
                    cursor.execute("""
                        INSERT INTO Users (full_name, email, password, role)
                        VALUES (?, ?, ?, ?)
                    """, (
                        full_name.strip(),
                        email.strip().lower(),         # store email in lowercase always
                        hashed_password.decode("utf-8"),
                        role
                    ))

                    conn.commit()
                    conn.close()

                    st.success(f"✅ Account created for {full_name}! Please login.")
                    st.balloons()

            except Exception as e:
                st.error(f"❌ Registration failed: {e}")

# Back link
st.markdown("<br>", unsafe_allow_html=True)
if st.button("← Back to Home"):
    st.switch_page("app.py")