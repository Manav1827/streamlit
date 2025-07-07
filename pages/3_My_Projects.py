import streamlit as st
import base64
import os
from firebase_utils import read_projects, update_project, delete_project
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(page_title="📁 My Projects", layout="wide")
st.title("🎬 My Projects")

# --- Auth Check ---
if "user" not in st.session_state or not st.session_state.user:
    st.error("🚫 Please log in to view your projects.")
    st.stop()

user_id = st.session_state.user["localId"]

# --- Fetch Projects ---
docs = read_projects(user_id)
ongoing, completed = [], []

for doc in docs:
    data = doc.to_dict()
    data["id"] = doc.id
    if data.get("status") == "completed":
        completed.append(data)
    else:
        ongoing.append(data)

# --- Project Display ---
def render_projects(projects, is_completed=False):
    for proj in projects:
        st.markdown("----")
        st.subheader(proj.get("title", "Untitled"))
        st.write(f"📁 Type: `{proj.get('type', 'unknown')}` | 🕒 Created: {proj.get('created_at', 'N/A')}")

        # Optional description or notes
        if "description" in proj:
            st.write(f"📝 {proj['description']}")

        # === Invitation GIF Preview ===
        if proj.get("type") == "invitation":
            gif_path = proj.get("meta", {}).get("output_path")
            if gif_path and os.path.exists(gif_path):
                with open(gif_path, "rb") as f:
                    gif_data = base64.b64encode(f.read()).decode()
                    st.markdown(f'<img src="data:image/gif;base64,{gif_data}" width="300">', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Preview not available (file missing).")

        # === Action Buttons ===
        col1, col2, col3 = st.columns([1, 1, 1])

        # ▶️ Resume for ongoing only
        if not is_completed:
            with col1:
                if st.button(f"▶️ Resume ({proj['id']})"):
                    st.session_state["resume_project"] = proj
                    st.switch_page("pages/2_Create_New.py")  # ✅ must be relative to root directory

            # Duplicate for ongoing only
            

            with col2:
                if st.button(f"✅ Mark Completed ({proj['id']})"):
                    update_project(user_id, proj["id"], {"status": "completed"})
                    st.rerun()

            with col3:
                if st.button(f"🗑 Delete ({proj['id']})"):
                    delete_project(user_id, proj["id"])
                    st.rerun()

        # Completed projects can only be deleted
        else:
            with col3:
                if st.button(f"🗑 Delete ({proj['id']})"):
                    delete_project(user_id, proj["id"])
                    st.rerun()

# --- Ongoing Projects ---
st.markdown("## 🟡 Ongoing Projects")
if ongoing:
    render_projects(ongoing, is_completed=False)
else:
    st.info("No ongoing projects found.")

# --- Completed Projects ---
st.markdown("## ✅ Completed Projects")
if completed:
    render_projects(completed, is_completed=True)
else:
    st.info("No completed projects yet.")
