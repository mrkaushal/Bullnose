import streamlit as st
from pymongo import MongoClient
from database import mongodb

def settings():
  collection = mongodb("config")

  st.title("Settings")

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
        
        collection.insert_one(data)
        st.write("Saved successfully!")
      else:
        st.write("Please enter valid api key and secret")

  with st.expander("**See Secret Details**"):
    # Show api key from mongodb bullnose database
    data = collection.find_one()

    # fetch api key and secret from mongodb
    api_key_fetch = data["api_key"]
    api_secret_fetch = data["api_secret"]
    api_key_historical_fetch = data["api_key_historical"]
    api_secret_historical_fetch = data["api_secret_historical"]

    st.write("**API Key** :: "+api_key_fetch)
    st.write("**API Secret** :: "+api_secret_fetch)
    st.write("**API Key Historical** :: "+api_key_historical_fetch)
    st.write("**API Secret Historical** :: "+api_secret_historical_fetch)