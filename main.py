import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

import cv2
# Streamlit options menu
from streamlit_option_menu import option_menu

from auth import login

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
    else:
        login_menu = "Login"
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Stock Prediction", "Other", "Settings","Contact", login_menu],
            icons=["house", "book", "back", "wrench","envelope", "shield-lock"],
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

        img_file_buffer = st.camera_input("Take a picture")

        if img_file_buffer is not None:
            # To read image file buffer with OpenCV:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

            # Check the type of cv2_img:
            # Should output: <class 'numpy.ndarray'>
            st.write(type(cv2_img))

            # Check the shape of cv2_img:
            # Should output shape: (height, width, channels)
            st.write(cv2_img.shape)


    elif selected == "Contact":
        contact()

    elif selected == "Login":
        login()
# Run the main function
if __name__ == "__main__":
    main()