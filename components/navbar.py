# import streamlit as st

# def show_navbar():
#     st.markdown(
#         """
#         <style>
#         .navbar {
#             background-color: #f0f2f6;
#             padding: 10px;
#             border-radius: 8px;
#         }
#         </style>
#         """, unsafe_allow_html=True
#     )


import streamlit as st
from auth import require_login


def show_navbar():
    require_login()
    with st.sidebar:
        st.image("assets/welcome_banner.png", width=150)  # Optional logo

        # 🔐 Auth Check
        if "user" not in st.session_state or st.session_state.user is None:
            st.warning("🚫 Please login to access the app.")
            st.info("🔐 Go to the main screen and login.")
            st.stop()  # 🚫 Stop further execution if not logged in

        # ✅ If logged in, show the navbar
        st.subheader(f"👋 Hello, {st.session_state.user.get('email', 'User')}")

        st.page_link("pages/2_Create_New.py", label="🎬 Start Creating", icon="🎥")
        st.page_link("pages/3_My_Projects.py", label="📁 My Projects", icon="📂")
        st.page_link("pages/4_Templates.py", label="📑 Templates", icon="🗂️")
        st.page_link("pages/5_Profile.py", label="👤 Profile & Settings", icon="⚙️")
        st.page_link("pages/6_Inspiration.py", label="🌟 Inspiration", icon="✨")

        st.divider()
        # 🔒 Add media permission revoker
        if st.button("🔒 Revoke Media Access"):
            st.session_state.media_permission = False
            st.info("🚫 Media access revoked.")
            
        if st.button("🚪 Logout"):
            st.session_state.page = "auth"
            st.session_state.user = None
