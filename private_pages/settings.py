import streamlit as st
from pymongo import MongoClient
from database import mongodb

def settings():
  config_collection = mongodb("config")
  user_collection = mongodb("api_users")

  st.title("Settings")

  tab1, tab2 = st.tabs(["API Keys", "API User Details"])

  with tab1:
    with st.form("settings_form", clear_on_submit=True):
      api_key=st.text_input('Enter your Api Key', max_chars=250)
      api_secret=st.text_input('Enter your Api Secret', max_chars=250)
      api_key_historical=st.text_input('Enter your Api Key for Historical Data', max_chars=250)
      api_secret_historical=st.text_input('Enter your Api Secret Historical Data', max_chars=250)

      if st.form_submit_button("Save"):
        # st.write(api_key)
        # st.write(api_secret)
        # Save api key to mongodb bullnose database
        if api_key and api_secret and api_key_historical and api_secret_historical:
          data = {"api_key":api_key,
                  "api_secret":api_secret,
                  "api_key_historical":api_key_historical,
                  "api_secret_historical":api_secret_historical
                  }
          
          config_collection.insert_one(data)
          st.success("Saved successfully!")
        else:
          st.warning("Please enter valid api key and secret")

    with st.expander("**See Secret Details**"):
      # Show api key from mongodb bullnose database
      data = config_collection.find_one()

      # fetch api key and secret from mongodb
      api_key_fetch = data["api_key"]
      api_secret_fetch = data["api_secret"]
      api_key_historical_fetch = data["api_key_historical"]
      api_secret_historical_fetch = data["api_secret_historical"]

      st.write("**API Key** :: "+api_key_fetch)
      st.write("**API Secret** :: "+api_secret_fetch)
      st.write("**API Key Historical** :: "+api_key_historical_fetch)
      st.write("**API Secret Historical** :: "+api_secret_historical_fetch)

  with tab2:
    with st.form("user_form", clear_on_submit=True):
      client_code = st.text_input('Enter your Client Code', max_chars=30)
      password = st.text_input('Enter your Password', max_chars=30, type="password")

      if st.form_submit_button("Save"):
        if client_code and password:
          data = {"client_code":client_code,
                  "password":password
                  }
          user_collection.insert_one(data)
          st.success("Saved successfully!")
        else:
          st.warning("Please enter valid client code and password")