import streamlit as st
import pandas as pd
import numpy as np
import plost
import json

# Streamlit extras
from streamlit_extras.no_default_selectbox import selectbox

from pages.user.stock_predict.smartWebSocketV2 import SmartWebSocketV2
from database import mongodb
# Fetch api_key from api_config collection where _id=2
client_code=mongodb("users").find_one({"_id":2})["username"]
api_key=mongodb("api_config").find_one({"_id":2})["api_key"]
feed_token=mongodb("api_sessions").find_one({"_id":2})["reg_ft"]
jwt_token=mongodb("api_sessions").find_one({"_id":2})["reg_jt"]
def real_time_predict():
    st.title("Real Time Stock Prediction")

    with open('json_files/OpenAPIScripMaster.json') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    with st.form("my_form"):
        # stock_name = st.selectbox('Select the stock', df['symbol'] + ' - ' + df['exch_seg'])
        stock_name = selectbox('Select the stock', df['symbol'] + ' - ' + df['exch_seg'], no_selection_label="Select.....")
        # Fetch the token from the selected stock
        token = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'token'].values[0]
        exch_seg = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'exch_seg'].values[0]
        
        AUTH_TOKEN = 'Bearer ' + jwt_token
        API_KEY = api_key
        CLIENT_CODE = client_code
        FEED_TOKEN = feed_token

        if st.form_submit_button("Submit"):

            correlation_id = "abc123"
            action = 1
            mode = 3

            token_list = [{"exchangeType": 1, "tokens": [token]}]

            sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)


            def on_data(wsapp, message):
                print("Ticks: {}".format(message))


            def on_open(wsapp):
                print("on open")
                sws.subscribe(correlation_id, mode, token_list)


            def on_error(wsapp, error):
                print(error)


            def on_close(wsapp):
                print("Close")


            # Assign the callbacks.
            sws.on_open = on_open
            sws.on_data = on_data
            sws.on_error = on_error
            sws.on_close = on_close

            sws.connect()