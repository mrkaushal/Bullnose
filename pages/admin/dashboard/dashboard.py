import json
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

# from . import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player

from . import Dashboard
from . import Editor
from . import Card
from . import DataGrid
from . import Radar
from . import Pie
from . import Player

def dash():

    st.title("Dashboard")
    
    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            data_grid=DataGrid(board, 6, 10, 15, 10, minH=4),
            pie=Pie(board, x=0, y=15, w=5, h=7, minH=4),
            radar=Radar(board, x=5, y=15, w=5, h=7, minH=4),
            player=Player(board, x=0, y=22, w=15, h=10, minH=8),
        )
        state.w = w

    else:
        w = state.w

    with elements("demo"):
        data_grid_data = json.dumps(DataGrid.DEFAULT_ROWS, indent=2)
        pie_data = json.dumps(Pie.DEFAULT_DATA, indent=2)
        radar_data = json.dumps(Radar.DEFAULT_DATA, indent=2)
        with w.dashboard(rowHeight=57):
            w.data_grid(data_grid_data)
            w.pie(pie_data)
            w.radar(radar_data)
            w.player()