import streamlit as st
import pandas as pd
import numpy as np

def stock_predict():
  st.title("Stock Prediction")
  st.write("Welcome to the stock prediction page")

  option = st.selectbox(
  'How would you like to be contacted?',
  ('RIL', 'LICI', 'SUNPHARMA'))

  uploaded_file = st.file_uploader("Choose a file")
  if uploaded_file is not None:
      # To read file as bytes:
      bytes_data = uploaded_file.getvalue()
      st.write(bytes_data)

      # To convert to a string based IO:
      stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
      st.write(stringio)

      # To read file as string:
      string_data = stringio.read()
      st.write(string_data)

      # Can be used wherever a "file-like" object is accepted:
      dataframe = pd.read_csv(uploaded_file)
      st.write(dataframe)

  # Simple line chart in streamlit
  chart_data = pd.DataFrame( np.random.randn(20, 3), columns=['a', 'b', 'c'])

  # Break line in streamlit
  st.write("")
  
  st.line_chart(chart_data)