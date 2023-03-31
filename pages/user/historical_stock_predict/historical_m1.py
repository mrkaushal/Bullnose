import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def model1(df):
    # Preprocessing the dataset
      X = df.iloc[:, 1:5].values
      y = df.iloc[:, -2].values

      # Splitting the dataset into training and testing sets
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

      # Training the Random Forest model
      rf = RandomForestRegressor(n_estimators=100, random_state=0)
      rf.fit(X_train, y_train)

      # Predicting future prices
      y_pred = rf.predict(X_test)
      st.write("Predicted Close Price:", y_pred)
      # Evaluating the model performance
      mse = mean_squared_error(y_test, y_pred)
      st.write("Mean Squared Error:", mse)