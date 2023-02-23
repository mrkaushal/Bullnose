import streamlit as st

def login():
    st.title("Login")
    st.write("Welcome to the login page")
    
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if username == "admin" and password == "admin":
                st.success("Logged in successfully!")
            else:
                st.warning("Incorrect username or password")