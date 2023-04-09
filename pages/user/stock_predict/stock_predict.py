import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Database
from database import mongodb
# Import SmartCannect API
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect


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
            ltp_data=obj.ltpData(exchange=exch_seg, tradingsymbol=tradingsymbol, symboltoken=token)

            st.write(ltp_data)
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

        except Exception as e:
            print("Historic Api failed: {}".format(e))
