import streamlit as st

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Inventory Optimization DSS",
    page_icon="📦",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        display: none;
    }

    </style>
    """, unsafe_allow_html=True)

# ==================================================
# SESSION
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==================================================
# LOGIN PAGE
# ==================================================

if not st.session_state.logged_in:

    st.markdown("""
    <div style='text-align:center;padding-top:50px;'>

    <h1>📦 Inventory Optimization DSS</h1>

    <h3>PT Mega Retail Indonesia</h3>

    <p>
    Decision Support System
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.subheader("🔐 Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if (
                username == "kelompok12"
                and
                password == "inventory12"
            ):

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error(
                    "Username atau Password salah"
                )

    st.stop()

# ==================================================
# DASHBOARD LANDING
# ==================================================

st.success("✅ Login berhasil")

st.title("📦 Inventory Optimization DSS")

st.write(
    "Pilih menu pada sidebar untuk mengakses dashboard."
)

if st.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.rerun()