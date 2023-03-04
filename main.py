import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

import navbar

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
    navbar.Navbar().sidebar()
# Run the main function
if __name__ == "__main__":
    main()