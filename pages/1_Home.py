import streamlit as st

# ---------------- CUSTOM CSS -----------------
st.markdown("""
<style>
/* General */
.stApp {
    background: linear-gradient(135deg, #6a85f1, #a777e3);
    color: black;
}
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Buttons */
button {
    background-color: #ff7f50;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    color: white;
    cursor: pointer;
    transition: 0.3s;
}
button:hover {
    background-color: #ff6333;
}

/* Floating Icons */
.floating-icons {
    position: fixed;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 16px;
    z-index: 1000;
}
.floating-icons div {
    background: rgba(255, 255, 255, 0.15);
    padding: 12px;
    border-radius: 16px;
    font-size: 22px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}
.card h3 {
    margin: 10px 0;
}
.card p {
    color: #ddd;
}

/* Centered */
.center {
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏠 Home")

st.page_link("pages/2_Create_New.py", label="➕ Create New Project", icon="🎬")
st.page_link("pages/3_My_Projects.py", label="📂 My Projects", icon="📁")
st.page_link("pages/4_Templates.py", label="🖼️ Explore Templates", icon="🗂️")
st.page_link("pages/5_Profile.py", label="⚙️ Profile/Settings", icon="👤")
st.page_link("pages/6_Inspiration.py", label="🌟 Inspiration", icon="✨")
