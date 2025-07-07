# import streamlit as st
# import os
# from theme import load_theme

# load_theme()

# st.set_page_config(page_title="🎨 Template Gallery", page_icon="📄", layout="wide")

# st.markdown("""
#     <h1 style='margin-bottom: 0;'>Template Gallery</h1>
#     <p style='color:gray;margin-top:0;'>Discover amazing designs</p>
# """, unsafe_allow_html=True)

# # ----------------- Template Database -----------------
# TEMPLATES = [
#     {"title": "Classic Birthday Invite", "category": "Birthday Invitations", "file": "b1.png", "tag": "new", "difficulty": "easy", "time": "1-2 hours"},
#     {"title": "Fun Birthday Invite", "category": "Birthday Invitations", "file": "b2.png", "difficulty": "easy", "time": "1 hour"},
#     {"title": "Elegant Wedding Invitation", "category": "Wedding Invitations", "file": "w1.png", "tag": "featured"},
#     {"title": "Floral Wedding Invite", "category": "Wedding Invitations", "file": "w2.png"},
  
#     {"title": "Adventure Travel Reel", "category": "Travel Reels", "file": "t1.png"},
#     {"title": "Travel Vlog Reel", "category": "Travel Reels", "file": "t2.png", "tag": "new"},
# ]   

# categories = ["All Categories"] + sorted(set(t["category"] for t in TEMPLATES))

# # ----------------- Search & Filter -----------------
# st.markdown("""
# <style>
# .search-container {
#     display: flex;
#     gap: 10px;
#     margin-bottom: 20px;
# }
# .search-input {
#     flex: 1;
# }
# </style>
# """, unsafe_allow_html=True)

# col1, col2 = st.columns([6, 2])
# with col1:
#     search_query = st.text_input("Search templates...", placeholder="Search templates")
# with col2:
#     selected_category = st.selectbox("Category", categories)

# # ----------------- Filter Templates -----------------
# filtered_templates = [
#     t for t in TEMPLATES
#     if (selected_category == "All Categories" or t["category"] == selected_category)
#     and (search_query.lower() in t["title"].lower())
# ]

# st.markdown(f"Found **{len(filtered_templates)}** templates in **{selected_category}**")

# # ----------------- Display Templates -----------------
# if filtered_templates:
#     cols = st.columns(3)
#     for idx, t in enumerate(filtered_templates):
#         with cols[idx % 3]:
#             st.markdown("""
#                 <div style='border-radius:15px;border:1px solid #e5e7eb;padding:15px;background:white;box-shadow:0 4px 12px rgba(0,0,0,0.06);'>
#             """, unsafe_allow_html=True)

#             st.image(f"assets/templates/{t['file']}", use_column_width=True)

#             # Title and Category
#             st.markdown(f"### {t['title']}")
#             st.caption(f"**{t['category']}**")

#             # Description
#             st.write("A beautiful template ready for customization.")

#             # Badges
#             badge_html = ""
#             if t.get("tag") == "new":
#                 badge_html += "<span style='background-color:#ecfdf5;color:#047857;padding:2px 8px;border-radius:9999px;font-size:12px;margin-right:5px;'>🆕 new</span>"
#             if t.get("tag") == "featured":
#                 badge_html += "<span style='background-color:#fef3c7;color:#92400e;padding:2px 8px;border-radius:9999px;font-size:12px;margin-right:5px;'>⭐ featured</span>"
#             if t.get("difficulty"):
#                 badge_html += "<span style='background-color:#dcfce7;color:#166534;padding:2px 8px;border-radius:9999px;font-size:12px;margin-right:5px;'>✔️ easy</span>"
#             if t.get("time"):
#                 badge_html += f"<span style='background-color:#f3f4f6;color:#374151;padding:2px 8px;border-radius:9999px;font-size:12px;'>⏱ {t['time']}</span>"

#             st.markdown(badge_html, unsafe_allow_html=True)

#             # Button
#             st.markdown("""
#                 <style>
#                 .use-template-button {
#                     background: linear-gradient(90deg, #6366f1, #9333ea);
#                     color: white;
#                     padding: 8px 16px;
#                     border: none;
#                     border-radius: 8px;
#                     cursor: pointer;
#                     font-size: 14px;
#                 }
#                 .use-template-button:hover {
#                     background: linear-gradient(90deg, #4f46e5, #7e22ce);
#                 }
#                 </style>
#             """, unsafe_allow_html=True)

#             if st.button("⚡ Use Template", key=f"use_{t['title']}"):
#                 st.success(f"✅ Selected {t['title']}")
#                 st.session_state["selected_template"] = t
#                 st.switch_page("4_Templates.py")

#             st.markdown("</div>", unsafe_allow_html=True)
# else:
#     st.info("No templates found matching your filters.")

# # ----------------- Summary Bar -----------------
# st.divider()
# st.markdown("""
# <div style='
#     display: flex;
#     justify-content: space-around;
#     background-color: white;
#     padding: 15px;
#     border-radius: 12px;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.05);
#     margin-top: 20px;
# '>
#     <div style='text-align:center;'>
#         <h2 style='color:#7c3aed;margin-bottom:5px;'>8</h2>
#         <p style='margin:0;color:gray;'>Total Templates</p>
#     </div>
#     <div style='text-align:center;'>
#         <h2 style='color:#059669;margin-bottom:5px;'>5</h2>
#         <p style='margin:0;color:gray;'>Categories</p>
#     </div>
#     <div style='text-align:center;'>
#         <h2 style='color:#f97316;margin-bottom:5px;'>2</h2>
#         <p style='margin:0;color:gray;'>Featured</p>
#     </div>
#     <div style='text-align:center;'>
#         <h2 style='color:#db2777;margin-bottom:5px;'>2</h2>
#         <p style='margin:0;color:gray;'>New Arrivals</p>
#     </div>
# </div>
# """, unsafe_allow_html=True)


import streamlit as st
st.markdown("""
<style>
/* ========== Base ========== */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
    scroll-behavior: smooth;
}
.stApp {
    background: linear-gradient(135deg, #fdfbfb, #ebedee);
    color: #2d3436;
    padding-bottom: 50px;
    overflow-x: hidden;
}

/* ========== Headings ========== */
h1, h2, h3, h4 {
    color: #6c5ce7;
    font-weight: 700;
    letter-spacing: 0.5px;
}
h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}
h2 {
    font-size: 1.75rem;
    margin-top: 2rem;
}

/* ========== Search Input ========== */
input[type="text"], .stTextInput input {
    background-color: #f9f9fb !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    border: 1px solid #dfe6e9 !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    font-size: 16px;
    transition: 0.3s ease-in-out;
}
input[type="text"]:focus {
    border-color: #a29bfe !important;
    box-shadow: 0 0 0 2px rgba(162, 155, 254, 0.3);
}

/* ========== Selectbox ========== */
.stSelectbox div {
    border-radius: 12px !important;
}

/* ========== Buttons ========== */
.stButton > button {
    background-color: #6c5ce7;
    color: white;
    font-weight: 600;
    font-size: 16px;
    border: none;
    padding: 0.5rem 1.3rem;
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(108, 92, 231, 0.2);
    transition: all 0.25s ease;
}
.stButton > button:hover {
    background-color: #341f97;
    transform: translateY(-2px);
}

/* ========== Card Grid ========== */
div[data-testid="column"] {
    padding: 0.5rem;
}
.card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    text-align: center;
    padding: 16px;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}
.card img {
    width: 100%;
    height: auto;
    border-radius: 12px;
    object-fit: cover;
    margin-bottom: 12px;
}
.card h3 {
    color: #2d3436;
    margin-bottom: 6px;
}
.card p {
    color: #636e72;
    font-size: 14.5px;
    margin-bottom: 8px;
}

/* ========== Alert Box Fix (e.g. use_column_width warnings) ========== */
.stAlert {
    border-radius: 12px;
    padding: 1rem 1.5rem;
    background-color: #fff3cd;
    color: #856404;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
    .card {
        text-align: center;
    }
    .stApp {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

import os
from theme import load_theme

load_theme()

st.set_page_config(page_title="🎨 Template Gallery", page_icon="📄", layout="wide")

# ----------------- Colorful Header -----------------
st.markdown("""
    <h1 style='margin-bottom: 0;
               background: linear-gradient(90deg, #6366f1, #ec4899);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;'>🎨 Template Gallery</h1>
    <p style='color:gray;margin-top:0;font-size:16px;'>Discover amazing designs that suit every vibe!</p>
""", unsafe_allow_html=True)

# ----------------- Template Database -----------------
TEMPLATES = [
    {"title": "Classic Birthday Invite", "category": "Birthday Invitations", "file": "b1.png", "tag": "new", "difficulty": "easy", "time": "1-2 hours"},
    {"title": "Fun Birthday Invite", "category": "Birthday Invitations", "file": "b2.png", "difficulty": "easy", "time": "1 hour"},
    {"title": "Elegant Wedding Invitation", "category": "Wedding Invitations", "file": "w1.png", "tag": "featured"},
    {"title": "Floral Wedding Invite", "category": "Wedding Invitations", "file": "w2.png"},
    {"title": "Adventure Travel Reel", "category": "Travel Reels", "file": "t1.png"},
    {"title": "Travel Vlog Reel", "category": "Travel Reels", "file": "t2.png", "tag": "new"},
]

categories = ["All Categories"] + sorted(set(t["category"] for t in TEMPLATES))

# ----------------- Search & Filter -----------------
st.markdown("""
<style>
.search-container {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
.search-input {
    flex: 1;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([6, 2])
with col1:
    search_query = st.text_input("Search templates...", placeholder="Search templates")
with col2:
    selected_category = st.selectbox("Category", categories)

# ----------------- Filter Templates -----------------
filtered_templates = [
    t for t in TEMPLATES
    if (selected_category == "All Categories" or t["category"] == selected_category)
    and (search_query.lower() in t["title"].lower())
]

st.markdown(f"Found **{len(filtered_templates)}** templates in **{selected_category}**")

# ----------------- Display Templates -----------------
if filtered_templates:
    cols = st.columns(3)
    for idx, t in enumerate(filtered_templates):
        with cols[idx % 3]:
            st.markdown(f"""
                <div style='
                    border-radius:15px;
                    border:1px solid #e0e7ff;
                    padding:15px;
                    background: linear-gradient(145deg, #ffffff, #f3f4f6);
                    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
                    transition: all 0.3s ease;
                '>
            """, unsafe_allow_html=True)

            st.image(f"assets/templates/{t['file']}", use_column_width=True)

            st.markdown(f"### {t['title']}")
            st.caption(f"**{t['category']}**")

            st.write("A beautiful template ready for customization.")

            # Badges
            badge_html = ""
            if t.get("tag") == "new":
                badge_html += "<span style='background: #fdf2f8;color:#be185d;padding:3px 10px;border-radius:9999px;font-size:12px;margin-right:5px;'>🆕 New</span>"
            if t.get("tag") == "featured":
                badge_html += "<span style='background: #fffbeb;color:#b45309;padding:3px 10px;border-radius:9999px;font-size:12px;margin-right:5px;'>⭐ Featured</span>"
            if t.get("difficulty"):
                badge_html += "<span style='background: #ecfdf5;color:#047857;padding:3px 10px;border-radius:9999px;font-size:12px;margin-right:5px;'>✔️ Easy</span>"
            if t.get("time"):
                badge_html += f"<span style='background: #eff6ff;color:#1d4ed8;padding:3px 10px;border-radius:9999px;font-size:12px;'>⏱ {t['time']}</span>"

            st.markdown(badge_html, unsafe_allow_html=True)

            # Button style
            st.markdown("""
                <style>
                .use-template-button {
                    background: linear-gradient(90deg, #6366f1, #ec4899);
                    color: white;
                    padding: 10px 18px;
                    border: none;
                    border-radius: 9999px;
                    font-size: 14px;
                    box-shadow: 0 4px 14px rgba(99,102,241,0.4);
                    transition: all 0.3s ease-in-out;
                }
                .use-template-button:hover {
                    transform: scale(1.05);
                    background: linear-gradient(90deg, #7c3aed, #f472b6);
                }
                </style>
            """, unsafe_allow_html=True)

            # Use Template Button
            st.markdown("<div class='use-template-button'>", unsafe_allow_html=True)
            if st.button("⚡ Use Template", key=f"use_{t['title']}"):
                st.success(f"✅ Selected {t['title']}")
                st.session_state["selected_template"] = t
                st.session_state["uploaded_template_file"] = os.path.join("assets", "templates", t["file"])
                st.switch_page("pages/4_Templates.py")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No templates found matching your filters.")

# ----------------- Summary Bar -----------------
st.divider()
st.markdown("""
<div style='
    display: flex;
    justify-content: space-around;
    background: linear-gradient(135deg, #f0fdfa, #e0f2fe);
    padding: 15px;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    margin-top: 30px;
'>
    <div style='text-align:center;'>
        <h2 style='color:#4f46e5;margin-bottom:5px;'>8</h2>
        <p style='margin:0;color:#374151;'>Total Templates</p>
    </div>
    <div style='text-align:center;'>
        <h2 style='color:#10b981;margin-bottom:5px;'>5</h2>
        <p style='margin:0;color:#374151;'>Categories</p>
    </div>
    <div style='text-align:center;'>
        <h2 style='color:#f59e0b;margin-bottom:5px;'>2</h2>
        <p style='margin:0;color:#374151;'>Featured</p>
    </div>
    <div style='text-align:center;'>
        <h2 style='color:#ec4899;margin-bottom:5px;'>2</h2>
        <p style='margin:0;color:#374151;'>New Arrivals</p>
    </div>
</div>
""", unsafe_allow_html=True)