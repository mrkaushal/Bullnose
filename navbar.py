import streamlit as st
import time

# Streamlit options menu
from streamlit_option_menu import option_menu

# Streamlit extra
from streamlit_extras.metric_cards import style_metric_cards

# Streamlit Auth
import streamlit_authenticator as stauth

# index page
from pages.public_pages.index import index

from pages.user.session.generate_session import generate_session

# Public Pages
from pages.user.home import home
from pages.public_pages.contact import contact

# Private Pages
from pages.user.settings import settings

#Stock Prediction
from pages.user.historical_stock_predict import historical_stock_predict
from pages.user.stock_predict.stock_predict import real_time_predict

# Admin Pages
from pages.admin.contact_form_list import contact_form_list
# Dash Pages
from pages.admin.dashboard.dashboard import dash
# User Pages
from pages.admin.user import add_user
from pages.admin.user.userboard import user_dash
# Database connection
from database import mongodb

class Navbar:
    def sidebar(self):
        # Sidebar menu
        # if user is logged in, show logout button
        if st.session_state.get("is_logged_in", True):
            # if is_admin then show admin menu
            if st.session_state.get("is_admin", False):
                with st.sidebar:
                    selected = option_menu(
                        menu_title="Menu",
                        options=["Dashboard", "Add User","User Dashboard",
                                 "Settings", "TOTP"],
                        icons=["house", "shield-lock", "envelope","wrench",
                               "envelope"],
                        menu_icon="cast",
                        default_index=0,
                        orientation="vertical",  # horizontal
                    )

                # Dashboard page
                if selected == "Dashboard":
                    dash()

                # Add User page
                elif selected == "Add User":
                    add_user.Users().add_user()

                elif selected == "User Dashboard":
                    user_dash()
                    
                elif selected == "Contact Details":
                    contact_form_list()

            # if not is_admin then show user menu
            else:
                with st.sidebar:
                    selected = option_menu(
                        menu_title="Menu",
                        options=["Home", "Historical","Stock Predict",
                                 "Settings", "Contact", "TOTP"],
                        icons=["house", "book", "bar-chart", "wrench",
                               "envelope", "book"],
                        menu_icon="cast",
                        default_index=0,
                        orientation="vertical",  # horizontal
                    )

                # Home page
                if selected == "Home":
                    home()

                # Stock Prediction page
                elif selected == "Historical":
                    hsp = historical_stock_predict
                    hsp.stock_predict()

                elif selected == "Stock Predict":
                    with st.spinner('Wait for it...'):
                        time.sleep(1)
                    real_time_predict()

                elif selected == "Settings":
                    settings()
                
                elif selected == "TOTP":
                    generate_session()

                elif selected == "Contact":
                    contact()