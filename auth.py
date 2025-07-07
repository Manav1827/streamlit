import streamlit as st

def require_login():
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("🚫 Please login to access this page.")
        st.stop()

def require_media_permission():
    if "media_permission" not in st.session_state:
        st.session_state.media_permission = False

    if not st.session_state.media_permission:
        st.subheader("🔐 Media Access Permission Required")
        st.info("This app requires access to your photos and videos to create reels and invitations.")

        if st.button("✅ Allow Media Access"):
            st.session_state.media_permission = True
            st.success("✅ Access Granted! You can now upload images/videos.")

        st.stop()  # 🚫 Stop the page until permission is granted