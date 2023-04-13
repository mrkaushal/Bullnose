import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Database
from database import mongodb
# Import SmartCannect API
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

def real_time_predict():
    st.title('Real Time Stock Prediction')
    # fetch current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # fetch yesterday date
    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d")

    api_key=mongodb("api_config").find_one({"_id":1})["api_key_historical"]

    user_record=mongodb("api_sessions").find_one({"_id":1})
    access_token=user_record["his_jt"]
    refresh_token=user_record["his_rt"]

    obj=SmartConnect(api_key=api_key, access_token=access_token, refresh_token=refresh_token)

    # import the csv file into a dataframe
    df = pd.read_csv('csv_files/CompanyList.csv')
    # Selectbox to select the stock
    stock_name = st.selectbox('Select the stock', df['symbol'] + ' - ' + df['exch_seg'])
    token = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'token'].values[0]
    exch_seg = df.loc[df['symbol'] + ' - ' + df['exch_seg'] == stock_name, 'exch_seg'].values[0]
    tradingsymbol = stock_name.split(' - ')[0]
    if st.button("Predict"):
        try:
            historicParam={
                "exchange": exch_seg,
                "symboltoken": str(token),
                "interval": "FIVE_MINUTE",
                "fromdate": yesterday_date+" 09:00", 
                "todate": current_date+" 15:30"
            }
            his_data = obj.getCandleData(historicParam)
            ltp_data=obj.ltpData(exchange=str(exch_seg), tradingsymbol=str(tradingsymbol), symboltoken=str(token))

            # st.write(ltp_data)
            # timestamp is current date and time in this format 2023-04-10T09:15:00+05:30
            ltp_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")#strftime("%Y-%m-%dT%H:%M:%S+05:30")
            ltp_open=ltp_data['data']['open']
            ltp_high=ltp_data['data']['high']
            ltp_low=ltp_data['data']['low']
            ltp_close=ltp_data['data']['close']
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
            for i in range(len(his_data['data'])):
                timestamp.append(his_data['data'][i][0])
                open_price.append(his_data['data'][i][1])
                high_price.append(his_data['data'][i][2])
                low_price.append(his_data['data'][i][3])
                close_price.append(his_data['data'][i][4])

            df = pd.DataFrame({
                'Timestamp': timestamp,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price
            })
            st.dataframe(df, use_container_width=True)
            # candles_df['range'] = candles_df['high'] - candles_df['low']
            df['Range'] = df['High'] - df['Low']

            train_df = df[:-1]  # Use all but the most recent candle for training
            test_df = df[-1:]   # Use the most recent candle for testing

            # Define the features we'll use to train the model
            features = ['Open', 'High', 'Low', 'Close', 'Range']

            # Create the model
            model = RandomForestRegressor(n_estimators=100, random_state=42)

            # Train the model
            model.fit(train_df[features], train_df['High'])

            # Create a dataframe with the values for the most recent candle
            current_candle_df = pd.DataFrame({
                'Open': [ltp_open],
                'High': [ltp_high],
                'Low': [ltp_low],
                'Close': [ltp_close],
                'Range': [ltp_high - ltp_low]
            })

            # Use the model to make predictions for the most recent candle
            predicted_high = model.predict(current_candle_df[features])[0]
            # predicted_low = model.predict(current_candle_df[features])[0]

            st.write("Predicted High: ", predicted_high)
            # st.write("Predicted Low: ", predicted_low)
        except Exception as e:
            print("Historic Api failed: {}".format(e))
