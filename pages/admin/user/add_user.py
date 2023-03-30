import streamlit as st

# Streamlit Auth
import streamlit_authenticator as stauth

# Database connection
from database import mongodb

class Users:

    def add_user(self):
        st.title("Add User")

        user_collection = mongodb("users")
        api_config_collection = mongodb("api_config")
        api_session_collection = mongodb("api_sessions")

        with st.expander("**Basic Information**", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name", type="default", max_chars=20)
                email = st.text_input("Email", type="default", max_chars=50)
                username = st.text_input("Username", type="default", max_chars=20, help="Please enter username of Angel Broking")
                password = st.text_input("Password", type="password", max_chars=10,)
                client_password = st.text_input("Client Password", type="password", max_chars=5, help="Please enter client password of Angel Broking")
            with col2:
                last_name = st.text_input("Last Name", type="default", max_chars=20)
                phone = st.text_input("Phone", type="default", max_chars=13)
                state = st.text_input("State", type="default", max_chars=20)
                confirm_password = st.text_input("Confirm Password", type="password", max_chars=10)
                client_password_confirm = st.text_input("Confirm Client Password", type="password", max_chars=5)

            if st.button("Save"):
                if first_name and last_name and email and phone and state and username and password and confirm_password:
                    if password == confirm_password:
                        # count no of id in database
                        if user_collection.count_documents({}) == 0:
                          user_id = 1
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
                              "client_password":client_password_confirm,
                              "is_active":True,
                              "is_admin":False
                              }
                          user_collection.insert_one(data)
                          # API Config
                          api_config_data = {
                              "_id":user_id,
                              "api_key":"demo",
                              "api_secret":"demo",
                              "api_key_historical":"demo",
                              "api_secret_historical":"demo",
                              }
                          api_config_collection.insert_one(api_config_data)
                          # API Session
                          api_session_data = {
                              "_id":user_id,
                              "reg_rt":"demo",
                              "reg_ft":"demo",
                              "reg_jt":"demo",
                              "his_rt":"demo",
                              "his_ft":"demo",
                              "his_jt":"demo",
                              }
                          api_session_collection.insert_one(api_session_data)
                          st.success("User added successfully!")
                        else:
                            if user_collection.count_documents({"username":username}) == 0:
                            # fetch the last user_id from database and add 1 to it
                                user_id = user_collection.find().sort("_id", -1).limit(1)[0]["_id"] + 1
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
                                    "client_password":client_password_confirm,
                                    "is_active":True,
                                    "is_admin":False
                                    }
                                user_collection.insert_one(data)
                                # API Config
                                api_config_data = {
                                    "_id":user_id,
                                    "api_key":"demo",
                                    "api_secret":"demo",
                                    "api_key_historical":"demo",
                                    "api_secret_historical":"demo",
                                    }
                                api_config_collection.insert_one(api_config_data)
                                # API Session
                                api_session_data = {
                                    "_id":user_id,
                                    "reg_rt":"demo",
                                    "reg_ft":"demo",
                                    "reg_jt":"demo",
                                    "his_rt":"demo",
                                    "his_ft":"demo",
                                    "his_jt":"demo",
                                    }
                                api_session_collection.insert_one(api_session_data)
                                st.success("User added successfully!")
                            else:
                                st.warning("Username already exists!")
                    else:
                        st.warning("Password and Confirm Password must be same!")
                else:
                    st.warning("Please enter valid details")

                

