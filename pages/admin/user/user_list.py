import json
import pandas as pd
import streamlit as st

# Database
from database import mongodb

def user_list():
    """
    Get user data from database
    """
    uc = mongodb("users")

    # fetch all users username and email
    users = uc.find({}, {"_id": 0,"name": 1, "username": 1, "email": 1, "phone": 1, "is_active": 1})
    df = pd.DataFrame(users)
    is_active = st.experimental_data_editor(df, use_container_width=True)

    is_active = is_active.loc[is_active['is_active'] == True]

    # Get active users where is_active = True
    active_users = is_active.to_dict('records')
    # Get inactive users from the dataframe where is_active = False
    inactive_users = df.loc[df['is_active'] == False].to_dict('records')
    # uc.update_many({}, {"$set": {"is_active": False}})
    if active_users == True:
        for user in active_users:
            uc.update_one({"username": user['username']}, {"$set": {"is_active": True}})