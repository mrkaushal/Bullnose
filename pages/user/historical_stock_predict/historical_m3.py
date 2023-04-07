import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import streamlit as st
def model3(data):
  # Extracting required columns from the response
  df = data[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]
  
  X = df[['open', 'high', 'low', 'volume']].values
  y = df['close'].values

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

  scaler = MinMaxScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  lr_model = LinearRegression()
  lr_model.fit(X_train_scaled, y_train)

  # First, get the latest stock data using Smart API - Angel One

  # Preprocess the latest data
  latest_data_processed = scaler.transform([[
      latest_data['open'],
      latest_data['high'],
      latest_data['low'],
      latest_data['volume']
  ]])

  # Use the model to predict the future price
  future_price = lr_model.predict(latest_data_processed)

  print(f'The predicted future price is: {future_price}')
