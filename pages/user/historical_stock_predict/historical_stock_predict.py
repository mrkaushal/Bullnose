import streamlit as st
import pandas as pd
import numpy as np
import json
import datetime
import time
import os

# Machine Learning Models
from pages.user.historical_stock_predict.historical_m1 import model1
from pages.user.historical_stock_predict.historical_m2 import model2
# Database
from database import mongodb

# Streamlit extras
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.mandatory_date_range import date_range_picker

# Import SmartCannect API
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)

# Streamlit echarts
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

# fetch current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
# fetch yesterday date
yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def stock_predict():
  # Fetch api_key from api_config collection where _id=2
  api_key=mongodb("api_config").find_one({"_id":1})["api_key_historical"]
  # find last record from api_sessions from _id column
  user_record=mongodb("api_sessions").find_one({"_id":1})
  access_token=user_record["his_jt"]
  refresh_token=user_record["his_rt"]

  #create object of call
  obj=SmartConnect(api_key=api_key, access_token=access_token, refresh_token=refresh_token)

  st.title("Historical Stock Prediction")
  # st.write("Welcome to the historical stock prediction page")

  # Read the data from json file
  with open('json_files/OpenAPIScripMaster.json') as f:
    data = json.load(f)

  # Convert the json data to columns and rows
  df = pd.DataFrame(data)
  nse_df = df[df['exch_seg'] == 'NSE']
  # Selectbox to select the stock
  stock_name = st.selectbox('Select the stock', df['symbol'] + ' - ' + nse_df['exch_seg'])
  result = date_range_picker("Select a date range",
                             default_start=datetime.datetime.now() - datetime.timedelta(days=3) ,
                             default_end=datetime.datetime.now(),
                             min_date=datetime.datetime.now() - datetime.timedelta(days=30),
                             max_date=datetime.datetime.now(),
                             error_message="Please select start and end date",
                            )
  # from date from result
  from_date = result[0]
  # to date from result
  to_date = result[1]
  
  # From date
  # from_date = st.date_input('From Date', datetime.datetime.now() - datetime.timedelta(days=1), min_value=datetime.datetime.now() - datetime.timedelta(days=30), max_value=datetime.datetime.now())
  from_date = from_date.strftime("%Y-%m-%d")+ " 09:00"
  # To date should be greater than from date
  # to_date = st.date_input('To Date', datetime.datetime.now(), min_value=datetime.datetime.now() - datetime.timedelta(days=30), max_value=datetime.datetime.now())
  to_date = to_date.strftime("%Y-%m-%d")+ " 15:30"

  # Selectbox to select the interval
  interval = st.selectbox('Select the interval', ['ONE_MINUTE', 'FIVE_MINUTE', 'FIFTEEN_MINUTE', 'THIRTY_MINUTE', 'ONE_HOUR', 'ONE_DAY'])

  # Selectbox to select the interval
  selected_model = st.selectbox('Select the model', ['Model M1', 'Model M2'])
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
      timestamp = []
      open_price = []
      high_price = []
      low_price = []
      close_price = []
      volume = []
      for i in range(len(his_data['data'])):
        timestamp.append(his_data['data'][i][0])
        open_price.append(his_data['data'][i][1])
        high_price.append(his_data['data'][i][2])
        low_price.append(his_data['data'][i][3])
        close_price.append(his_data['data'][i][4])
        volume.append(his_data['data'][i][5])

      df = pd.DataFrame({
        'Timestamp': timestamp,
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Close': close_price,
        'Volume': volume
      })
      st.dataframe(df, use_container_width=True)
      
      if selected_model == 'Model M1':
        model1(df)
      elif selected_model == 'Model M2':
        model2(df)
      else:
        st.write("Model M3")
      # Generate the line chart for the stock with the dates on x-axis and the price on y-axis
      # st.line_chart(data=df[['Open', 'High', 'Low', 'Close']],
      #               use_container_width=True,
      #               height=500
      #               )
      
    except Exception as e:
      print("Historic Api failed: {}".format(e.message))
