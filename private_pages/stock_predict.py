import streamlit as st
import pandas as pd
import numpy as np
import json

# Dtabase
from database import mongodb

# Import SmartCannect API
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)
api_key=mongodb("config").find_one()["api_key_historical"]
access_token=mongodb("api_sessions").find_one()["his_jt"]
refresh_token=mongodb("api_sessions").find_one()["his_rt"]
#create object of call
obj=SmartConnect(api_key=api_key, access_token=access_token, refresh_token=refresh_token)

# Streamlit echarts
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

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

  # Fetch the token from the selected stock
  token = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'token'].values[0]
  exch_seg = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'exch_seg'].values[0]

  try:
    historicParam={
    "exchange": exch_seg,
    "symboltoken": token,
    "interval": "ONE_MINUTE",
    "fromdate": "2021-02-01 09:00", 
    "todate": "2023-02-25 09:16"
    }
    his_data = obj.getCandleData(historicParam)
    # st.write(his_data)
    # Generate the DataFrame from the data
    df = pd.DataFrame(his_data['data'])
    # st.dataframe(df)
    
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
    st.dataframe(df)
    index = pd.to_datetime(df['Dates'])
    print(index)
    # Generate the line chart for the stock with the dates on x-axis and the price on y-axis
    st.line_chart(data=df[['Open', 'High', 'Low', 'Close']],
                  use_container_width=True,
                  height=500
                  )
    
  except Exception as e:
      print("Historic Api failed: {}".format(e.message))

