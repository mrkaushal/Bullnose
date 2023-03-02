import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time

import cv2
# Streamlit options menu
from streamlit_option_menu import option_menu

# Streamlit extra 
from streamlit_extras.metric_cards import style_metric_cards

from auth import login
from generate_session import generate_session

# Public Pages
from public_pages.home import home
from public_pages.contact import contact
# Private Pages
from private_pages.settings import settings
from private_pages.stock_predict import stock_predict

# Admin Pages
from pages.admin.contact_form_list import contact_form_list

# Title and icon
im = Image.open("media/favicon.ico")
logo = Image.open("media/logo-full.png")

st.set_page_config(
    page_title="Bullnose",
    page_icon=im,
    layout="wide", # centered
    initial_sidebar_state="expanded", # collapsed
    menu_items={
        'Get Help': 'https://kaushalpatel.info',
        'Report a bug': "https://kaushalpatel.info",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def main():
    # Sidebar menu
    # if user is logged in, show logout button
    if st.session_state.get("logged_in", True):
        login_menu = "Logout"
        with st.sidebar:
            selected = option_menu(
                menu_title="Menu",
                options=["Home", "Stock Prediction", "Settings","Contact Details","TOTP", login_menu],
                icons=["house", "book", "wrench","envelope", "book","shield-lock"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical", # horizontal
            )
    else:
        login_menu = "Login"
        with st.sidebar:
            selected = option_menu(
                menu_title="Menu",
                options=["Home", "Stock Prediction", "Settings","Contact","TOTP", login_menu],
                icons=["house", "book", "wrench","envelope", "book","shield-lock"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical", # horizontal
            )

    # Home page
    if selected == "Home":
        home()

    # Stock Prediction page
    elif selected == "Stock Prediction":
        with st.spinner('Wait for it...'):
            time.sleep(1)
        stock_predict()

    elif selected == "Settings":
        settings()

    elif selected == "Contact":
        contact()

    elif selected == "Contact Details":
        contact_form_list()

    elif selected == "TOTP":
        generate_session()

    elif selected == "Login":
        login()
# Run the main function
if __name__ == "__main__":
    main()