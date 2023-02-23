import streamlit as st
import pandas as pd
import numpy as np

def stock_predict():
  st.title("Stock Prediction")
  st.write("Welcome to the stock prediction page")

  option = st.selectbox(
  'How would you like to be contacted?',
  ('RIL', 'LICI', 'SUNPHARMA'))


  if option == 'RIL':
    uploaded_file = st.file_uploader("Choose a file", type="csv")
    if uploaded_file is not None:
      csv_read = pd.read_csv(uploaded_file, parse_dates=True, index_col=0)
      # st.dataframe(df, use_container_width=True)  # Same as st.write(df)

      df = pd.DataFrame(
        columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"],
        data=csv_read,
      )

      st.dataframe(df, use_container_width=True)  # Same as st.write(df)

      # convert date column to text

      st.line_chart(df[['Open', 'High', 'Close']])