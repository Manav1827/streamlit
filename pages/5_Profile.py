# import streamlit as st
# from auth import require_login
# from components import navbar

# require_login()  # 🔐 User must be logged in
# navbar.show_navbar()

# import streamlit as st

# st.set_page_config(page_title="👤 Profile & Settings", page_icon="⚙️", layout="wide")

# st.title("👤 Profile & Settings")

# # ---------------------- User Information ----------------------
# st.subheader("👤 User Information")

# if "user" in st.session_state:
#     user_info = st.session_state.user
#     st.markdown(f"**Name:** `{user_info.get('displayName', 'N/A')}`")
#     st.markdown(f"**Email:** `{user_info.get('email', 'N/A')}`")
#     st.markdown(f"**User ID:** `{user_info.get('localId', 'N/A')}`")
# else:
#     st.warning("🚫 You are not logged in.")

# st.markdown("---")

# # ---------------------- Subscription ----------------------
# st.subheader("💳 Subscription Details")

# subscription_type = st.selectbox(
#     "Subscription Plan",
#     ["Free", "Pro (Premium)", "Enterprise"],
#     index=0,
#     help="Upgrade to unlock premium templates and features."
# )

# if subscription_type != "Free":
#     st.success("🎉 You have access to premium features!")

# st.markdown("---")

# # ---------------------- App Settings ----------------------
# st.subheader("⚙️ App Settings")

# col1, col2 = st.columns(2)

# with col1:
#     dark_mode = st.toggle("🌙 Enable Dark Mode")
#     notifications = st.toggle("🔔 Enable Notifications")

# with col2:
#     if st.button("🧹 Clear Cache & Reset"):
#         st.cache_data.clear()
#         st.cache_resource.clear()
#         st.session_state.clear()
#         st.success("🧹 Cache cleared. Session reset.")


# st.markdown("---")

# # ---------------------- Help & Support ----------------------
# st.subheader("❓ Help & Support")

# with st.expander("📄 FAQ"):
#     st.markdown("""
# **Q1:** How to use templates?  
# ➡️ Go to the Templates page and select a template to start.

# **Q2:** How to save my project?  
# ➡️ When you create an invitation or reel, it automatically saves to My Projects.

# **Q3:** How to contact support?  
# ➡️ Use the Contact Support section below.
# """)

# with st.expander("📧 Contact Support"):
#     st.markdown("""
# - 📧 Email: support@yourapp.com  
# - 📱 WhatsApp: +91-XXXXXXXXXX  
# - 🌐 Website: [www.yourapp.com](https://www.yourapp.com)
# """)

# st.markdown("---")

# # ---------------------- Legal ----------------------
# st.subheader("📜 Terms & Privacy")

# with st.expander("📃 Terms & Conditions"):
#     st.markdown("""
# By using this app, you agree to not misuse or distribute the generated content for illegal purposes. All templates are for personal and commercial use with proper licenses.
# """)

# with st.expander("🔒 Privacy Policy"):
#     st.markdown("""
# We respect your privacy. Your data is securely stored and not shared with third parties. You can request data deletion by contacting support.
# """)


#working

# import streamlit as st
# from auth import require_login
# from components import navbar


# # ---------------- Navbar & Login ----------------
# require_login()
# navbar.show_navbar()

# st.set_page_config(page_title="👤 Profile & Settings", page_icon="⚙️", layout="wide")
# st.title("👤 Profile & Settings")

# # ---------------- Dark Mode Functions ----------------
# def apply_dark_mode():
#     st.markdown(
#         """
#         <style>
#         body {background-color: #0e1117; color: white;}
#         .stApp {background-color: #0e1117;}
#         header, .css-1avcm0n, .css-18ni7ap {background-color: #0e1117;}
#         .stButton>button {background-color: #333; color: white;}
#         .stTextInput>div>div>input {background-color: #333; color: white;}
#         .stSelectbox>div>div>div {background-color: #333; color: white;}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# def apply_light_mode():
#     st.markdown(
#         """
#         <style>
#         body {background-color: white; color: black;}
#         .stApp {background-color: white;}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# # --------------- Theme Settings ----------------
# st.subheader("🌗 App Theme")

# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = False

# theme_toggle = st.toggle("🌙 Enable Dark Mode", value=st.session_state.dark_mode)

# if theme_toggle:
#     st.session_state.dark_mode = True
#     apply_dark_mode()
# else:
#     st.session_state.dark_mode = False
#     apply_light_mode()

# st.markdown("---")


# # ---------------- User Info ----------------
# st.subheader("👤 User Information")

# if "user" in st.session_state:
#     user_info = st.session_state.user
#     st.markdown(f"**Name:** `{user_info.get('displayName', 'N/A')}`")
#     st.markdown(f"**Email:** `{user_info.get('email', 'N/A')}`")
#     st.markdown(f"**User ID:** `{user_info.get('localId', 'N/A')}`")
# else:
#     st.warning("🚫 You are not logged in.")

# st.markdown("---")


# # ---------------- Subscription ----------------
# st.subheader("💳 Subscription Details")

# subscription_type = st.selectbox(
#     "Subscription Plan",
#     ["Free", "Pro (Premium)", "Enterprise"],
#     index=0,
#     help="Upgrade to unlock premium templates and features.",
# )

# if subscription_type != "Free":
#     st.success("🎉 You have access to premium features!")

# st.markdown("---")


# # ---------------- App Settings ----------------
# st.subheader("⚙️ App Settings")

# col1, col2 = st.columns(2)

# with col1:
#     notifications = st.toggle("🔔 Enable Notifications")

# with col2:
#     if st.button("🧹 Clear Cache & Reset"):
#         st.cache_data.clear()
#         st.cache_resource.clear()
#         st.session_state.clear()
#         st.success("🧹 Cache cleared. Session reset.")

# st.markdown("---")


# # ---------------- Help & Support ----------------
# st.subheader("❓ Help & Support")

# with st.expander("📄 FAQ"):
#     st.markdown(
#         """
# **Q1:** How to use templates?  
# ➡️ Go to the Templates page and select a template.

# **Q2:** How to save my project?  
# ➡️ When you create an invitation or reel, it automatically saves to My Projects.

# **Q3:** How to contact support?  
# ➡️ Use the Contact Support section below.
# """
#     )

# with st.expander("📧 Contact Support"):
#     st.markdown(
#         """
# - 📧 Email: support@yourapp.com  
# - 📱 WhatsApp: +91-XXXXXXXXXX  
# - 🌐 Website: [www.yourapp.com](https://www.yourapp.com)
# """
#     )

# st.markdown("---")


# # ---------------- Legal ----------------
# st.subheader("📜 Terms & Privacy")

# with st.expander("📃 Terms & Conditions"):
#     st.markdown(
#         """
# By using this app, you agree not to misuse or distribute the generated content for illegal purposes.  
# All templates are for personal and commercial use with proper licenses.
# """
#     )

# with st.expander("🔒 Privacy Policy"):
#     st.markdown(
#         """
# We respect your privacy.  
# Your data is securely stored and not shared with third parties.  
# You can request data deletion by contacting support.
# """
#     )


# st.markdown("---")


# # ---------------- Logout ----------------
# st.subheader("🚪 Logout")

# if st.button("🚪 Logout"):
#     st.session_state.clear()
#     st.success("✅ You have been logged out. Please refresh the page.")



import streamlit as st
from auth import require_login
from components import navbar

# -------------- App Config --------------
st.set_page_config(page_title="👤 Profile & Settings", layout="wide")
require_login()
navbar.show_navbar()


# -------------- Custom CSS --------------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3, h4, h5, h6, p {
        color: white;
    }
    .sidebar-container {
        background-color: #111827;
        color: black;
        padding: 1rem;
        height: 100vh;
        border-radius: 8px;
    }
    .section-card {
        background-color: #1f2937;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .input-box {
        background-color: #374151;
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .sidebar-button {
        background-color: #1f2937;
        color: white;
        border: none;
        padding: 0.7rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.6rem;
        width: 100%;
        text-align: left;
        font-weight: 500;
    }
    .sidebar-button:hover {
        background-color: #2563eb;
    }
    .logout-button {
        background-color: #dc2626;
        color: white;
        padding: 0.6rem;
        border: none;
        border-radius: 6px;
        margin-top: 2rem;
        width: 100%;
    }
    select {
        background-color: #374151;
        color: white;
        padding: 0.5rem;
        border-radius: 6px;
    }
    .toggle-switch {
        margin-top: 0.5rem;
        margin-bottom: 1.2rem;
    }
    

    </style>
""", unsafe_allow_html=True)


# -------------- Layout --------------
col_sidebar, col_main = st.columns([1, 4])

# -------- Sidebar --------
with col_sidebar:
    st.markdown("<div class='sidebar-container'>", unsafe_allow_html=True)
    st.markdown("### 👤 Profile & Settings")
    if st.button("👤 Profile", use_container_width=True):
        st.session_state.view = "profile"
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.view = "settings"
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", type="primary"):
        st.session_state.clear()
        st.success("✅ Logged out successfully.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------- Main Section --------
with col_main:
    view = st.session_state.get("view", "profile")

    if view == "profile":
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("👤 Profile Information")
        if "user" in st.session_state:
            user = st.session_state.user
            st.markdown(f"<div class='input-box'><b>Name:</b> {user.get('displayName', 'John Doe')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='input-box'><b>Email:</b> {user.get('email', 'john.doe@example.com')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='input-box'><b>User ID:</b> {user.get('localId', 'user_123456789')}</div>", unsafe_allow_html=True)
        else:
            st.warning("🚫 User not logged in.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("💳 Subscription Details")
        st.markdown("<div class='input-box'><b>Current Plan:</b> Free</div>", unsafe_allow_html=True)
        plan = st.selectbox("Subscription Plan", ["Free", "Pro (Premium)", "Enterprise"])
        if plan != "Free":
            st.success("🎉 You have access to premium features!")
        st.markdown("</div>", unsafe_allow_html=True)

    elif view == "settings":
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("🌗 App Theme")
        theme = st.toggle("🌙 Enable Dark Mode", key="dark_mode_toggle")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("⚙️ App Settings")
        st.toggle("🔔 Enable Notifications")
        if st.button("🧹 Clear Cache & Reset"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.clear()
            st.success("🧹 Cache cleared. Session reset.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("❓ Help & Support")
        with st.expander("📄 FAQ"):
            st.markdown("""
                **Q1:** How to use templates?  
                ➡️ Go to the Templates page and select a template.

                **Q2:** How to save my project?  
                ➡️ Projects save automatically in My Projects.

                **Q3:** How to contact support?  
                ➡️ Use the Contact Support section below.
            """)
        with st.expander("📧 Contact Support"):
            st.markdown("""
                - 📧 Email: support@yourapp.com  
                - 📱 WhatsApp: +91-XXXXXXXXXX  
                - 🌐 Website: [www.yourapp.com](https://www.yourapp.com)
            """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("📜 Terms & Privacy")
        with st.expander("📃 Terms & Conditions"):
            st.markdown("""
            By using this app, you agree not to misuse or distribute the generated content for illegal purposes.  
            All templates are for personal and commercial use with proper licenses.
            """)
        with st.expander("🔒 Privacy Policy"):
            st.markdown("""
            We respect your privacy.  
            Your data is securely stored and not shared with third parties.  
            You can request data deletion by contacting support.
            """)
        st.markdown("</div>", unsafe_allow_html=True)
