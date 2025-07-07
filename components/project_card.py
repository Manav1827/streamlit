import streamlit as st
from database import db
from datetime import datetime

def display_project_card(name, details):
    thumbnail = details.get("thumbnail", "assets/default_thumbnail.png")
    last_modified = details.get("last_modified", "Unknown Date")
    project_type = details.get("type", "Unknown")

    with st.container():
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(thumbnail, width=120)

        with col2:
            st.subheader(name)
            st.caption(f"🗂️ {project_type} | 🕓 Last Modified: {last_modified}")

            col_btn1, col_btn2, col_btn3 = st.columns(3)

            with col_btn1:
                if st.button("▶️ Resume", key=f"resume_{name}"):
                    st.session_state["current_project"] = name
                    st.switch_page("pages/editor.py")

            with col_btn2:
                if st.button("📄 Duplicate", key=f"duplicate_{name}"):
                    db.duplicate_project(name)
                    st.experimental_rerun()

            with col_btn3:
                if st.button("🗑️ Delete", key=f"delete_{name}"):
                    db.delete_project(name)
                    st.experimental_rerun()

        st.markdown("---")
