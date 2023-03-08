from database import mongodb
import streamlit as st
import streamlit_authenticator as stauth


def main():
    print("Hello World")
    user_collection = mongodb("users")
    api_config_collection = mongodb("api_config")
    api_session_collection = mongodb("api_sessions")

    # Create a user
    admin_password = stauth.Hasher("admin").generate()
    admin_data = {
        "_id":1,
        "name":"admin",
        "email":"abc@abc.com",
        "phone":"1234567890",
        "state":"Delhi",
        "username":"admin",
        "password":admin_password,
        "client_password":"",
        "is_active":True,
        "is_admin":True
    }
    user_collection.insert_one(admin_data)

    # Create a user
    user_password = stauth.Hasher("user@123").generate()
    user_data = {
        "_id":2,
        "name":"user",
        "email":"user@abc.com",
        "phone":"1234567890",
        "state":"Delhi",
        "username":"K50494801",
        "password":user_password,
        "client_password":"1379",
        "is_active":True,
        "is_admin":False
    }
    user_collection.insert_one(user_data)

    # Api config
    api_config_data = {
        "_id":2,
        "api_key":"BrEiEdJz",
        "api_secret":"91713f45-f4fd-4a6e-bd2c-8014e1819d0f",
        "api_key_historical":"NRlI1dza",
        "api_secret_historical":"f9449778-22be-4ee0-8e4c-dfa21bf88b26",
    }
    api_config_collection.insert_one(api_config_data)

    # Api session
    api_session_data = {
        "_id":2,
        "reg_rt":"demo",
        "reg_ft":"demo",
        "reg_jt":"demo",
        "his_rt":"demo",
        "his_ft":"demo",
        "his_jt":"demo",
    }
    api_session_collection.insert_one(api_session_data)

if __name__ == "__main__":
    main()
