import streamlit as st

# Streamlit Auth
import streamlit_authenticator as stauth
# Import the Database
from database import mongodb

def login():
    st.title("Login")
    st.write("Welcome to the login page")
    
    # ----------------------------- User Authentication ----------------------------- #
        # user collection from database
    uc = mongodb("users")
    # all usernames and passwords from database
    
    # authenticator = stauth.Authenticate()
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            uc_details = uc.find_one({"username":username})
            print(uc_details.username)
            print(uc_details.password)