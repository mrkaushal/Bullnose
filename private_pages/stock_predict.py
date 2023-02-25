import streamlit as st
import pandas as pd
import numpy as np
import json

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

