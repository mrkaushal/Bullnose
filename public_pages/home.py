import streamlit as st
from PIL import Image
from streamlit_echarts import st_echarts
import json
from streamlit_echarts import JsCode
import time
# Streamlit Elements
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo
from streamlit_extras.metric_cards import style_metric_cards

def home():
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Gain", value=5000, delta=1000)
    col2.metric(label="Loss", value=5000, delta=-1000)
    col3.metric(label="No Change", value=5000, delta=0)
    style_metric_cards(border_left_color="#ff4b4b")
    with elements("html_container"):
        # Html Container
        st.markdown(
            """
            <div style="background-color:#f5f5f5; padding: 10px; border-radius: 10px;">
                <h1 style="color: #000000; text-align: center;">Welcome to the BullNose - Stock Analysis</h1>
                <p style="color: #000000; text-align: center;">This is a sample dashboard</p>
                <img src="https://media.giphy.com/media/3o7TKsQ8UQJhIYq6WU/giphy.gif" alt="BullNose" style="width:100%;height:100%;">
            </div>
            """,
            unsafe_allow_html=True,
        )
    # with elements("dashboard"):

    #     # First, build a default layout for every element you want to include in your dashboard
    #     layout = [
    #         # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
    #         # saved layout will be restored automatically
    #         dashboard.Item("Home", 0, 0, 2, 2, moved=True, resized=True),
    #     ]
    #     # saved layout
    #     # with open("layout.json", "r") as f:
    #     #     layout = json.load(f)

    #     # If you want to retrieve updated layout values as the user move or resize dashboard items,
    #     # you can pass a callback to the onLayoutChange event parameter.

    #     def handle_layout_change(updated_layout):
    #         # You can save the layout in a file, or do anything you want with it.
    #         # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
    #         print(updated_layout)
    #         # save the layout in a file
    #         with open("layout.json", "w") as f:
    #             json.dump(updated_layout, f)
            
    #         return updated_layout

    #     # Then, pass the layout to the dashboard.Grid() component.

    #     with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
    #         # Finally, add your dashboard items.
    #         with mui.Paper(elevation=3, variant="outlined", square=True):
    #             mui.TextField(
    #                 label="My text input",
    #                 defaultValue="Type here",
    #                 variant="outlined",
    #             )
    #             mui.Collapse(in_=True)

            



