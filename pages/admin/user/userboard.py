import json
import streamlit as st

from streamlit import session_state as state
from streamlit_elements import elements
from types import SimpleNamespace

from pages.admin.user.user_list import user_list

def user_dash():
    st.title("User Dashboard")

    # Get user data
    user_list()