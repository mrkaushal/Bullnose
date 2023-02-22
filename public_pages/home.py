import streamlit as st
from PIL import Image

logo = Image.open("media/favicon.ico")
def home():
    st.title("Dashboard")
    st.write("Welcome to the home Page")
    st.image(logo, width=100, caption="Bullnose")