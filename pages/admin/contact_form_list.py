import streamlit as st
import pandas as pd
from database import mongodb

def contact_form_list():
    st.title("Contact Form List")

    collection = mongodb("contact")
    data = collection.find()
    
    # Show all the data in table format with Name, Email, Message columns
    name = []
    email = []
    message = []
    for i in data:
        name.append(i["name"])
        email.append(i["email"])
        message.append(i["message"])

    df = pd.DataFrame({"Name": name, "Email": email, "Message": message})
    st.dataframe(df, use_container_width=True)