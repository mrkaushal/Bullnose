import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def model2(df):

  # split the data into input features and target variable
  X = df.drop(['Timestamp','Open', 'Close'], axis=1)
  y = df[['Open', 'Close']]

  # st.dataframe(X)
  # st.dataframe(y)
  # split the data into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # create a linear regression model and fit it to the training data
  try:
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    st.write("Model Trained")
  except Exception as e:
    st.write(e)

  # make predictions on the testing data
  y_pred = lr_model.predict(X_test)

  # evaluate the performance of the model
  mse = mean_squared_error(y_test, y_pred)
  r2 = r2_score(y_test, y_pred)
  st.write('Mean squared error:', mse)
  st.write('R-squared:', r2)

  # make a prediction for a new set of input features
  new_data = pd.DataFrame({
      'High': [2245],
      'Low': [2211.25],
      'Volume': [159000]
  })
  prediction = lr_model.predict(new_data)
  # store the prediction in open and close columns with rounded values
  new_data['Open'] = np.round(prediction[0][0], 2)
  new_data['Close'] = np.round(prediction[0][1], 2)
  st.write('Predicted Values:', new_data)