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

from auth import login
from pages.user.session.generate_session import generate_session

# Public Pages
from pages.user.home import home
from pages.public_pages.contact import contact

# Private Pages
from pages.user.settings import settings
from pages.user.stock_predict import stock_predict

# Admin Pages
from pages.admin.contact_form_list import contact_form_list
# Dash Pages
from pages.admin.dashboard.dashboard import dash
# User Pages
from pages.admin.user import add_user


class Navbar:

    def sidebar(self):
        # Sidebar menu
        # if user is logged in, show logout button
        if st.session_state.get("logged_in", True):
            login_menu = "Logout"
            # if is_admin then show admin menu
            if st.session_state.get("is_admin", False):
                with st.sidebar:
                    selected = option_menu(
                        menu_title="Menu",
                        options=["Dashboard", "Add User",
                                 "Settings", "TOTP", login_menu],
                        icons=["house", "shield-lock", "wrench",
                               "envelope", "shield-lock"],
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

                elif selected == "Contact Details":
                    contact_form_list()

            # if not is_admin then show user menu
            else:
                with st.sidebar:
                    selected = option_menu(
                        menu_title="Menu",
                        options=["Home", "Stock Prediction",
                                 "Settings", "Contact", "TOTP", login_menu],
                        icons=["house", "book", "wrench",
                               "envelope", "book", "shield-lock"],
                        menu_icon="cast",
                        default_index=0,
                        orientation="vertical",  # horizontal
                    )

                # Home page
                if selected == "Home":
                    home()

                # Stock Prediction page
                elif selected == "Stock Prediction":
                    with st.spinner('Wait for it...'):
                        time.sleep(1)
                    sp = stock_predict
                    sp.stock_predict()

                elif selected == "Settings":
                    settings()
                
                elif selected == "TOTP":
                    generate_session()

                elif selected == "Contact":
                    contact()

        # if user is not logged in, show login button
        else:
            login_menu = "Login"
            with st.sidebar:
                selected = option_menu(
                    menu_title="Menu",
                    options=["Home", "Contact", login_menu],
                    icons=["house", "envelope", "shield-lock"],
                    menu_icon="cast",
                    default_index=0,
                    orientation="vertical",  # horizontal
                )

            # Home page
            if selected == "Home":
                index()

            # Contact page
            if selected == "Contact":
                contact()
            
            # Login page
            elif selected == "Login":
                login()
