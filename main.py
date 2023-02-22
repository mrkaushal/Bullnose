import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
# Streamlit options menu
from streamlit_option_menu import option_menu

# Public Pages
from public_pages.home import home
from public_pages.contact import contact
# Private Pages
from private_pages.settings import settings
from private_pages.stock_predict import stock_predict

# Title and icon
im = Image.open("media/favicon.ico")
st.set_page_config(
    page_title="Bullnose",
    page_icon=im,
    layout="wide",
    initial_sidebar_state="expanded", # collapsed
)
# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Stock Prediction", "Other", "Settings","Contact"],
        icons=["house", "book", "back", "wrench","envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical", # horizontal
    )

# Home page
if selected == "Home":
    home()

# Stock Prediction page
elif selected == "Stock Prediction":
    stock_predict()

elif selected == "Settings":
    settings()

# Other page
elif selected == "Other":
    st.title("Other")
    st.write("Getting continous data of stock")

elif selected == "Contact":
    contact()