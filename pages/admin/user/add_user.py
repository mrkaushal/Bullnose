import streamlit as st

# Streamlit Auth
import streamlit_authenticator as stauth

# Database connection
from database import mongodb

class Users:

    def add_user(self):
        st.title("Add User")

        collection = mongodb("users")

        with st.expander("**Basic Information**", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name", type="default", max_chars=20)
                email = st.text_input("Email", type="default", max_chars=50)
                username = st.text_input("Username", type="default", max_chars=20, help="Please enter username of Angel Broking")
                password = st.text_input("Password", type="password", max_chars=10, help="Please enter password of Angel Broking")

            with col2:
                last_name = st.text_input("Last Name", type="default", max_chars=20)
                phone = st.text_input("Phone", type="default", max_chars=13)
                state = st.text_input("State", type="default", max_chars=20)
                confirm_password = st.text_input("Confirm Password", type="password", max_chars=10)

            if st.button("Save"):
                if first_name and last_name and email and phone and state and username and password and confirm_password:
                    if password == confirm_password:
                        # check if username already exists if yes, show warning message
                        if collection.count_documents({"username":username}) == 0:
                          user_id = collection.count_documents({}) + 1
                          password = stauth.Hasher(password).generate()
                          data = {
                              "_id":user_id, # "_id" is a default key in MongoDB, so we can't use it as a key in our data. So we use "user_id" as a key and "_id" as a value.
                              "first_name":first_name,
                              "last_name":last_name,
                              "email":email,
                              "phone":phone,
                              "state":state,
                              "username":username,
                              "password":password,
                              "is_active":True,
                              "is_admin":False
                              }
                          collection.insert_one(data)
                          st.success("User added successfully!")
                        else:
                          st.warning("Username already exists!")
                    else:
                        st.warning("Password and Confirm Password must be same!")
                else:
                    st.warning("Please enter valid details")

                

