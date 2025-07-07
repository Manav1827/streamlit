import streamlit as st
from auth import require_login
from components import navbar

require_login()  # 🔐 User must be logged in
navbar.show_navbar()


st.title("🌟 Inspiration Gallery")

st.markdown("Explore public projects from our community!")

st.image("https://via.placeholder.com/400x200.png?text=Inspiration+1", caption="Travel Reel")
st.image("https://via.placeholder.com/400x200.png?text=Inspiration+2", caption="Wedding Invite")
st.image("https://via.placeholder.com/400x200.png?text=Inspiration+3", caption="Birthday Video")
