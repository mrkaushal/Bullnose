import json
import requests
import socket
import uuid
import re
import time
import streamlit as st

import streamlit_authenticator as stauth


# Database
from database import mongodb

# User Collection
user_collection = mongodb("users")
# Session Collection
session_collection = mongodb("api_sessions")
# config Collection
config_collection = mongodb("api_config")

def generate_session():

    with st.form("session_data", clear_on_submit=True):
        totp_str = st.text_input("TOTP", type="password", help="Enter the TOTP from your authenticator app", placeholder="123456", max_chars=6)
        # check whether the totp is integer or not
        if totp_str.isdigit():
            totp = int(totp_str)
        else:
            totp = 000000
        
        if st.form_submit_button("Submit"):
            if totp:
                # st.write(totp)
                # st.write(type(totp))
                st.success("Logged in successfully!")

                # Fetch the password from database
                collection = mongodb("users")
                data = collection.find_one({"username":"admin"})

                try:
                  # Get the client's public IP address
                  clientPublicIp = " " + requests.get('https://api.ipify.org').text
                  if " " in clientPublicIp:
                      clientPublicIp = clientPublicIp.replace(" ","")
                except Exception as e:
                    print("Exception while retrieving public IP address, using default value", e)
                    clientPublicIp = "106.193.147.98"  # default value if unable to retrieve
                try:
                    # Get the client's local IP address
                    hostname = socket.gethostname()
                    clientLocalIp = socket.gethostbyname(hostname)
                except Exception as e:
                    print("Exception while retrieving local IP address, using default value", e)
                    clientLocalIp = "127.0.0.1"  # default value if unable to retrieve
                try:
                    # Get the client's MAC address
                    clientMacAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
                except Exception as e:
                    print("Exception while retrieving MAC address, using default value", e)
                    clientMacAddress = "00:00:00:00:00:00"  # default value if unable to retrieve

                url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
                # Find Client Code and Password from database where id = 2
                user_data = user_collection.find_one({"_id":2})
                payload = {
                    "clientcode": user_data["username"],
                    "password": user_data["client_password"],
                    "totp": totp,
                }
                headers_regular = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-UserType": "USER",
                    "X-SourceID": "WEB",
                    "X-ClientLocalIP": clientLocalIp,
                    "X-ClientPublicIP": clientPublicIp,
                    "X-MACAddress": clientMacAddress,
                    "X-PrivateKey": config_collection.find_one()["api_key_historical"],
                }
                reg_response = requests.post(url, headers=headers_regular, data=json.dumps(payload))
                reg_data = reg_response.json()

                regular_refreshToken = reg_data['data']['refreshToken']
                regular_feedToken = reg_data['data']['feedToken']
                regular_jwtToken = reg_data['data']['jwtToken']

                headers_historical = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-UserType": "USER",
                    "X-SourceID": "WEB",
                    "X-ClientLocalIP": clientLocalIp,
                    "X-ClientPublicIP": clientPublicIp,
                    "X-MACAddress": clientMacAddress,
                    "X-PrivateKey": config_collection.find_one()["api_key_historical"],
                }
                his_response = requests.post(url, headers=headers_historical, data=json.dumps(payload))
                his_data = his_response.json()

                historical_refreshToken = his_data['data']['refreshToken']
                historical_feedToken = his_data['data']['feedToken']
                historical_jwtToken = his_data['data']['jwtToken']

                # session_collection.insert_one(data)
                
                # session id counter
                session_id = 2
                # check if session id exists then increment it by 1
                if session_collection.find_one({"_id": session_id}):
                    # Update the data
                    data = {
                        "_id": session_id,
                        "reg_rt": regular_refreshToken,
                        "reg_ft": regular_feedToken,
                        "reg_jt": regular_jwtToken,
                        "his_rt": historical_refreshToken,
                        "his_ft": historical_feedToken,
                        "his_jt": historical_jwtToken,
                    }
                    session_collection.update_one({"_id": session_id}, {"$set": data})
                else:
                    # Insert the data
                    data = {
                        "_id": session_id,
                        "reg_rt": regular_refreshToken,
                        "reg_ft": regular_feedToken,
                        "reg_jt": regular_jwtToken,
                        "his_rt": historical_refreshToken,
                        "his_ft": historical_feedToken,
                        "his_jt": historical_jwtToken,
                    }
                    session_collection.insert_one(data)
                    print("Record not found")
                    print("Record {sid} inserted successfully".format(sid=session_id))
            else:
                st.warning("Please enter valid details")