import streamlit as st
import pandas as pd
import numpy as np
import websocket as ws
import asyncio

def real_time_predict():
    st.title('Real Time Stock Prediction')
    # import the csv file into a dataframe
    df = pd.read_csv('csv_files/CompanyList.csv')
    st.write(df)
    # Selectbox to select the stock
    stock_name = st.selectbox('Select the stock', df['symbol'] + ' - ' + df['exch_seg'])
    st.write(stock_name)
    token =  df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'token'].values[0]
    exch_seg = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'exch_seg'].values[0]
    st.write(str(token))
    st.write(exch_seg)