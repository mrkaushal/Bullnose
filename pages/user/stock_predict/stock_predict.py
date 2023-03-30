import streamlit as st
import pandas as pd
import numpy as np
import websocket as ws
import asyncio

async def real_time_predict():
    st.title('Real Time Stock Prediction')

    async with ws.connect('ws://192.46.210.179:8000/symbols-data/') as websocket:
        while True:
            response = await websocket.recv()
            st.write(response)