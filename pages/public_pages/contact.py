import streamlit as st
from database import mongodb

def contact():
    st.title("Contact")

    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        message = st.text_area("Message")
    
        if st.form_submit_button("Send"):
            if name and email and message:
                collection = mongodb("contact")
                contact_id = collection.count_documents({}) + 1
                data = {
                    "_id":contact_id, # "_id" is a default key in MongoDB, so we can't use it as a key in our data. So we use "contact_id" as a key and "_id" as a value.
                    "name":name,
                    "email":email,
                    "phone":phone,
                    "message":message,
                    "is_read":False
                    }
                collection.insert_one(data)
                st.success("Message sent successfully!")
            else:
                st.warning("Please enter valid details")