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
                data = {"name":name,
                        "email":email,
                        "phone":phone,
                        "message":message
                        }
                collection.insert_one(data)
                st.success("Message sent successfully!")
            else:
                st.warning("Please enter valid details")