import streamlit as st
import os
from theme import load_theme
load_theme()


st.set_page_config(page_title="🎨 Templates", page_icon="📄", layout="wide")

st.title("🎨 Explore Templates")

# ----------------- Template Database -----------------
TEMPLATES = [
    {"title": "Elegant Wedding Invitation", "category": "Wedding Invitations", "file": "w1.png", "tag": "featured"},
    {"title": "Classic Birthday Invite", "category": "Birthday Invitations", "file": "b1.png", "tag": "new"},
    {"title": "Travel Vlog Reel", "category": "Travel Reels", "file": "t1.png", "tag": "featured"},
    {"title": "Adventure Travel Reel", "category": "Travel Reels", "file": "t2.png"},

    {"title": "Floral Wedding Invite", "category": "Wedding Invitations", "file": "w2.png"},
    {"title": "Fun Birthday Invite", "category": "Birthday Invitations", "file": "b2.png"},
]

categories = sorted(set(t["category"] for t in TEMPLATES))

# ----------------- Search Bar -----------------
search_query = st.text_input("🔍 Search Templates", "")

# ----------------- Featured / New -----------------
st.subheader("🌟 Featured Templates")
featured = [t for t in TEMPLATES if t.get("tag") == "featured"]
if featured:
    cols = st.columns(len(featured))
    for col, t in zip(cols, featured):
        with col:
            st.image(f"assets/templates/{t['file']}", use_column_width=True)
            st.caption(f"**{t['title']}**")
else:
    st.info("No featured templates.")

st.subheader("🆕 New Arrivals")
new_arrivals = [t for t in TEMPLATES if t.get("tag") == "new"]
if new_arrivals:
    cols = st.columns(len(new_arrivals))
    for col, t in zip(cols, new_arrivals):
        with col:
            st.image(f"assets/templates/{t['file']}", use_column_width=True)
            st.caption(f"**{t['title']}**")
else:
    st.info("No new templates.")

st.markdown("---")

# ----------------- Template by Categories -----------------
for cat in categories:
    st.subheader(f"📂 {cat}")
    filtered = [
        t for t in TEMPLATES
        if cat.lower() in t["category"].lower()
           and search_query.lower() in t["title"].lower()
    ]
    if filtered:
        cols = st.columns(3)
        for idx, t in enumerate(filtered):
            with cols[idx % 3]:
                st.image(f"assets/templates/{t['file']}", use_column_width=True)
                st.caption(f"**{t['title']}**")
                if st.button(f"Use Template: {t['title']}", key=f"use_{t['title']}"):
                    st.success(f"✅ Selected {t['title']}")
                    st.session_state["selected_template"] = t
                    st.switch_page("4_Templates.py")  # ✔️ If using multipage
    else:
        st.info(f"No templates found in {cat} matching '{search_query}'.")
