import json,sys
import streamlit as st
# import requests

def mainpage():
    st.sidebar.markdown("### Menu")

    # Streamlit App Title
    st.title("Solar 7 - Help the Climate Change")
    st.markdown('an Open Source Project')

    # Input Address
    address = st.text_input("Enter an Address to search in Google Maps API:")
