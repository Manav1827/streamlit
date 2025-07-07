# import streamlit as st
# import base64
# import os
# from firebase_utils import read_projects, update_project, delete_project

# st.set_page_config(page_title="📁 My Projects", layout="wide")

# st.markdown("""
#     <h1 style='margin-bottom: 5px;'>My Projects</h1>
#     <p style='color:gray;margin-top:0;'>Manage your creative work</p>
# """, unsafe_allow_html=True)

# # 🔐 Authentication Check
# if "user" not in st.session_state or not st.session_state.user:
#     st.error("🚫 Please log in to view your projects.")
#     st.stop()

# user_id = st.session_state.user["localId"]

# # 🔍 Fetch Projects
# docs = read_projects(user_id)
# ongoing, completed = [], []

# for doc in docs:
#     data = doc.to_dict()
#     data["id"] = doc.id
#     if data.get("status") == "completed":
#         completed.append(data)
#     else:
#         ongoing.append(data)

# # ================== Render Project Card =====================
# def render_project_card(proj, is_completed=False):
#     st.markdown(
#         """
#         <style>
#         .card {
#             border: 1px solid #e5e7eb;
#             border-radius: 15px;
#             padding: 20px;
#             background-color: white;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.05);
#             margin-bottom: 20px;
#         }
#         .badge {
#             display: inline-block;
#             padding: 2px 8px;
#             border-radius: 9999px;
#             font-size: 12px;
#             margin-right: 5px;
#         }
#         .badge-type {
#             background-color: #eef2ff;
#             color: #3730a3;
#         }
#         .badge-status {
#             background-color: #dcfce7;
#             color: #166534;
#         }
#         .delete-button {
#             background-color: #fee2e2;
#             color: #b91c1c;
#             padding: 6px 14px;
#             border: none;
#             border-radius: 8px;
#             cursor: pointer;
#             font-size: 14px;
#         }
#         .delete-button:hover {
#             background-color: #fecaca;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown("<div class='card'>", unsafe_allow_html=True)

#     st.markdown(f"<h3 style='margin-bottom:8px;'>{proj.get('title', 'Untitled')}</h3>", unsafe_allow_html=True)

#     st.markdown(
#         f"<span class='badge badge-type'>{proj.get('type', 'other')}</span>"
#         f"<span class='badge badge-status'>{'completed' if is_completed else 'ongoing'}</span>",
#         unsafe_allow_html=True
#     )

#     st.markdown(f"<p style='color:gray;font-size:14px;margin-top:8px;'>🗓️ Created: {proj.get('created_at', 'N/A')}</p>", unsafe_allow_html=True)
#     st.markdown(f"<p style='margin-top:10px;'>{proj.get('description', 'No description provided.')}</p>", unsafe_allow_html=True)

#     # ==== Action Buttons ====
#     col1 = st.columns(1)[0]
#     with col1:
#         delete_button = st.button(
#             "🗑 Delete",
#             key=f"delete_{proj['id']}"
#         )
#         if delete_button:
#             delete_project(user_id, proj["id"])
#             st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)


# # ================== Tabs for Ongoing and Completed ====================
# tab1, tab2 = st.tabs(["Ongoing", "Completed"])

# with tab1:
#     if ongoing:
#         for proj in ongoing:
#             render_project_card(proj, is_completed=False)
#     else:
#         st.info("No ongoing projects found.")

# with tab2:
#     if completed:
#         for proj in completed:
#             render_project_card(proj, is_completed=True)
#     else:
#         st.info("No completed projects yet.")

# # ================== Summary Bar =========================
# total_count = len(ongoing) + len(completed)

# st.markdown("""
# <div style='
#     display: flex;
#     justify-content: space-around;
#     background-color: white;
#     padding: 15px;
#     border-radius: 12px;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.05);
#     margin-top: 30px;
# '>
#     <div style='text-align:center;'>
#         <h2 style='color:#4f46e5;margin-bottom:5px;'>""" + str(total_count) + """</h2>
#         <p style='margin:0;color:gray;'>Total Projects</p>
#     </div>
#     <div style='text-align:center;'>
#         <h2 style='color:#f97316;margin-bottom:5px;'>""" + str(len(ongoing)) + """</h2>
#         <p style='margin:0;color:gray;'>In Progress</p>
#     </div>
#     <div style='text-align:center;'>
#         <h2 style='color:#10b981;margin-bottom:5px;'>""" + str(len(completed)) + """</h2>
#         <p style='margin:0;color:gray;'>Completed</p>
#     </div>
# </div>
# """, unsafe_allow_html=True)

#2222222 working version
import streamlit as st
import base64
import os
from firebase_utils import read_projects, update_project, delete_project
from streamlit_extras.switch_page_button import switch_page
st.markdown("""
<style>
/* ========== GLOBAL RESET ========== */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    scroll-behavior: smooth;
}

/* ========== APP BACKGROUND ========== */
.stApp {
    background: linear-gradient(135deg, #eef2f3, #d9a7c7);
    color: #2c3e50;
    padding-bottom: 50px;
}

/* ========== HEADER ========== */
h1, h2, h3, h4 {
    color: #5f27cd;
    font-weight: 700;
}

/* ========== BUTTONS ========== */
button, .stButton>button {
    background-color: #ff6b6b;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    color: #fff;
    font-weight: 600;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    transition: 0.3s ease;
}
button:hover, .stButton>button:hover {
    background-color: #ee5253;
    transform: translateY(-1px);
}

/* ========== TAGS & BADGES ========== */
.tag {
    display: inline-block;
    padding: 4px 12px;
    margin: 2px;
    font-size: 12px;
    font-weight: 500;
    border-radius: 12px;
    background-color: #c8d6e5;
    color: #1e272e;
}
.tag.completed {
    background-color: #b8e994;
    color: #006400;
}
.tag.ongoing {
    background-color: #ffeaa7;
    color: #e17055;
}

/* ========== PROJECT CARD ========== */
.project-card {
    background: #ffffffdd;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    transition: all 0.25s ease-in-out;
}
.project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
}
.project-card h4 {
    margin-bottom: 10px;
    color: #2d3436;
}
.project-card p {
    color: #636e72;
    font-size: 15px;
}

/* ========== DELETE BUTTON ========== */
.delete-btn {
    background-color: #d63031 !important;
    color: white;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 14px;
    font-weight: 600;
    transition: 0.2s ease-in-out;
}
.delete-btn:hover {
    background-color: #c0392b !important;
}

/* ========== SEARCH INPUTS ========== */
input[type="text"], textarea {
    border-radius: 14px !important;
    padding: 10px 16px !important;
    border: 1px solid #ccc !important;
    transition: 0.2s ease;
    box-shadow: none !important;
}
input[type="text"]:focus {
    border-color: #7f8c8d !important;
}

/* ========== FLOATING ICONS ========== */
.floating-icons {
    position: fixed;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 14px;
    z-index: 1000;
}
.floating-icons div {
    background: rgba(255, 255, 255, 0.25);
    padding: 12px;
    border-radius: 14px;
    font-size: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.3s;
}
.floating-icons div:hover {
    transform: scale(1.1);
    background: rgba(255, 255, 255, 0.4);
}

/* ========== CENTER ALIGN ========== */
.center {
    text-align: center;
    margin: 1rem auto;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="📁 My Projects", layout="wide")

st.markdown("""
    <h1 style='margin-bottom: 5px; color:#6366f1;'>📁 My Projects</h1>
    <p style='color:gray;margin-top:0;'>Manage your creative work beautifully</p>
""", unsafe_allow_html=True)

# ================== CSS Styling ==========================
st.markdown("""
<style>
/* Card Styling */
.card {
    border: 2px solid #e5e7eb;
    border-radius: 18px;
    padding: 20px;
    background-color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 25px;
    transition: transform 0.2s ease;
}
.card:hover {
    transform: scale(1.02);
}

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 12px;
    margin-right: 6px;
    font-weight: 600;
}
.badge-type {
    background-color: #e0f2fe;
    color: #0369a1;
}
.badge-status {
    background-color: #dcfce7;
    color: #166534;
}
.badge-ongoing {
    background-color: #fef9c3;
    color: #92400e;
}

/* Delete Button */
.stButton > button {
    background: linear-gradient(to right, #f43f5e, #be123c);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 14px;
    cursor: pointer;
    transition: background 0.3s ease;
}
.stButton > button:hover {
    background: linear-gradient(to right, #be123c, #881337);
}
</style>
""", unsafe_allow_html=True)

# 🔐 Authentication Check
if "user" not in st.session_state or not st.session_state.user:
    st.error("🚫 Please log in to view your projects.")
    st.stop()

user_id = st.session_state.user["localId"]

# 🔍 Fetch Projects
docs = read_projects(user_id)
ongoing, completed = [], []

for doc in docs:
    data = doc.to_dict()
    data["id"] = doc.id
    if data.get("status") == "completed":
        completed.append(data)
    else:
        ongoing.append(data)


# ================== Render Project Card =====================
def render_project_card(proj, is_completed=False):
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='margin-bottom:8px;'>{proj.get('title', 'Untitled')}</h3>", unsafe_allow_html=True)

    badge_status = 'badge-status' if is_completed else 'badge-ongoing'
    st.markdown(
        f"<span class='badge badge-type'>{proj.get('type', 'other').capitalize()}</span>"
        f"<span class='badge {badge_status}'>{'Completed' if is_completed else 'Ongoing'}</span>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='color:gray;font-size:14px;margin-top:8px;'>🗓️ Created: {proj.get('created_at', 'N/A')}</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='margin-top:10px;'>{proj.get('description', 'No description provided.')}</p>",
        unsafe_allow_html=True
    )

    # --- Invitation GIF Preview ---
    if proj.get("type") == "invitation":
        gif_path = proj.get("meta", {}).get("output_path")
        if gif_path and os.path.exists(gif_path):
            with open(gif_path, "rb") as f:
                gif_data = base64.b64encode(f.read()).decode()
                st.markdown(f'<img src="data:image/gif;base64,{gif_data}" width="300">', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Preview not available (file missing).")

    col1, col2, col3 = st.columns([1, 1, 1])

    if not is_completed:
        with col1:
            if st.button(f"▶️ Resume ({proj['id']})", key=f"resume_{proj['id']}"):
                st.session_state["resume_project"] = proj
                switch_page("pages/2_Create_New.py")

        with col2:
            if st.button(f"✅ Mark Completed ({proj['id']})", key=f"complete_{proj['id']}"):
                update_project(user_id, proj["id"], {"status": "completed"})
                st.rerun()

        with col3:
            if st.button(f"🗑 Delete", key=f"delete_{proj['id']}"):
                delete_project(user_id, proj["id"])
                st.rerun()
    else:
        with col3:
            if st.button(f"🗑 Delete", key=f"delete_{proj['id']}"):
                delete_project(user_id, proj["id"])
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================== Tabs for Ongoing and Completed ====================
tab1, tab2 = st.tabs(["🟨 Ongoing", "✅ Completed"])

with tab1:
    if ongoing:
        cols = st.columns(2)
        for idx, proj in enumerate(ongoing):
            with cols[idx % 2]:
                render_project_card(proj, is_completed=False)
    else:
        st.info("🚀 No ongoing projects found.")

with tab2:
    if completed:
        cols = st.columns(2)
        for idx, proj in enumerate(completed):
            with cols[idx % 2]:
                render_project_card(proj, is_completed=True)
    else:
        st.info("✅ No completed projects yet.")

# ================== Summary Bar =========================
# total_count = len(ongoing) + len(completed)

# st.markdown(f"""
# <div style='
#     display: flex;
#     justify-content: space-around;
#     background-color: white;
#     padding: 20px;
#     border-radius: 20px;
#     box-shadow: 0 4px 16px rgba(0,0,0,0.08);
#     margin-top: 30px;
# '>
#     <div style='text-align:center;'>
#         <h2 style='color:#6366f1;margin-bottom:5px;'>{total_count}</h2>
#         <p style='margin:0;color:gray;'>Total Projects</p>
#     </div>

#     <div style='text-align:center;'>
#         <h2 style='color:#f59e0b;margin-bottom:5px;'>{len(ongoing)}</h2>
#         <p style='margin:0;color:gray;'>Ongoing</p>
#     </div>

#     <div style='text-align:center;'>
#         <h2 style='color:#10b981;margin-bottom:5px;'>{len(completed)}</h2>
#         <p style='margin:0;color:gray;'>Completed</p>
#     </div>

# </div>
# """, unsafe_allow_html=True)

