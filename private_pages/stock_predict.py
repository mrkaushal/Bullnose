import streamlit as st
import pandas as pd
import numpy as np
import json
import datetime
import time
import os
# Database
from database import mongodb

# Streamlit extras
from streamlit_extras.no_default_selectbox import selectbox

# Import SmartCannect API
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)
api_key=mongodb("config").find_one()["api_key_historical"]
# find last record from api_sessions from _id column
last_record=mongodb("api_sessions").find().sort("_id", -1).limit(1)
access_token=last_record[0]["his_jt"]
refresh_token=last_record[0]["his_rt"]

#create object of call
obj=SmartConnect(api_key=api_key, access_token=access_token, refresh_token=refresh_token)

# Streamlit echarts
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

# fetch current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
# fetch yesterday date
yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def stock_predict():
  
  st.title("Stock Prediction")
  st.write("Welcome to the stock prediction page")

  # Read the data from json file
  with open('json_files/OpenAPIScripMaster.json') as f:
    data = json.load(f)

  # Convert the json data to columns and rows
  df = pd.DataFrame(data)
  # Selectbox to select the stock
  stock_name = st.selectbox('Select the stock', df['symbol'] + ' - ' + df['exch_seg'])
 
  # From date
  from_date = st.date_input('From Date', datetime.datetime.now() - datetime.timedelta(days=1))
  from_date = from_date.strftime("%Y-%m-%d")+ " 09:00"
  # To date
  to_date = st.date_input('To Date', datetime.datetime.now())
  to_date = to_date.strftime("%Y-%m-%d")+ " 15:30"

  # Selectbox to select the interval
  interval = st.selectbox('Select the interval', ['ONE_MINUTE', 'FIVE_MINUTE', 'FIFTEEN_MINUTE', 'THIRTY_MINUTE', 'ONE_HOUR', 'ONE_DAY'])
  # Fetch the token from the selected stock
  token = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'token'].values[0]
  exch_seg = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'exch_seg'].values[0]

  if st.button("Submit"):
    try:
      historicParam={
      "exchange": exch_seg,
      "symboltoken": token,
      "interval": interval,
      "fromdate": from_date, 
      "todate": to_date
      }
      his_data = obj.getCandleData(historicParam)
      # st.write(his_data)
      # Generate the DataFrame from the data
      df = pd.DataFrame(his_data['data'])
      # st.dataframe(df, use_container_width=True)
      
      # Generate the dates list
      dates = []
      open_price = []
      high_price = []
      low_price = []
      close_price = []
      volume = []
      for i in range(len(his_data['data'])):
        dates.append(his_data['data'][i][0])
        open_price.append(his_data['data'][i][1])
        high_price.append(his_data['data'][i][2])
        low_price.append(his_data['data'][i][3])
        close_price.append(his_data['data'][i][4])
        volume.append(his_data['data'][i][5])

      df = pd.DataFrame({
        'Dates': dates,
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Close': close_price,
        'Volume': volume
      })
      st.dataframe(df, use_container_width=True)
      # Generate the line chart for the stock with the dates on x-axis and the price on y-axis
      # st.line_chart(data=df[['Open', 'High', 'Low', 'Close']],
      #               use_container_width=True,
      #               height=500
      #               )
      
    except Exception as e:
      print("Historic Api failed: {}".format(e.message))
