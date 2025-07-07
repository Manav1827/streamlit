# theme.py

import streamlit as st

def apply_dark_mode():
    dark_css = """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    header, .css-1avcm0n, .css-18ni7ap {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #333;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #333;
        color: white;
    }
    .stSelectbox>div>div>div {
        background-color: #333;
        color: white;
    }
    .stTextArea>div>textarea {
        background-color: #333;
        color: white;
    }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)


def apply_light_mode():
    light_css = """
    <style>
    body {
        background-color: white;
        color: black;
    }
    .stApp {
        background-color: white;
    }
    </style>
    """
    st.markdown(light_css, unsafe_allow_html=True)


def load_theme():
    """Call this function at the top of every page."""
    if "dark_mode" in st.session_state and st.session_state.dark_mode:
        apply_dark_mode()
    else:
        apply_light_mode()
