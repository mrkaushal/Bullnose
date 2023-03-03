import json

from streamlit_elements import mui
from .dash import Dashboard

# Database
from database import mongodb

class DataGrid(Dashboard.Item):

    collection = mongodb("contact")
    data = collection.find()

    cid = []
    name = []
    email = []
    message = []

    for i in data:
        cid.append(i["_id"])
        name.append(i["name"])
        email.append(i["email"])
        message.append(i["message"])

    DEFAULT_COLUMNS = [
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'name', "headerName": 'Name', "width": 150, "editable": False, },
        { "field": 'email', "headerName": 'Email', "type": 'email', "width": 220, "editable": False, },
        { "field": 'message', "headerName": 'Message', "type": 'textarea', "width": 500, "editable": False, },
    ]
    DEFAULT_ROWS = []
    for i in range(len(cid)):
        DEFAULT_ROWS.append({"id": cid[i], "name": name[i], "email": email[i], "message": message[i]})

    def _handle_edit(self, params):
        print(params)

    def __call__(self, json_data):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DEFAULT_ROWS

        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.ViewCompact()
                mui.Typography("Contact List")

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                mui.DataGrid(
                    columns=self.DEFAULT_COLUMNS,
                    rows=data,
                    pemailSize=5,
                    rowsPerPemailOptions=[5],
                    checkboxSelection=True,
                    disableSelectionOnClick=True,
                    onCellEditCommit=self._handle_edit,
                )
