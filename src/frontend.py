import json,sys
import streamlit as st
from src.backend import * 

# import requests

def mainpage():
    st.sidebar.markdown("### Menu")

    # Streamlit App Title
    st.title("Solar 7 - Help the Climate Change")
    st.markdown('an Open Source Project')

    # Input Address
    address = st.text_input("Enter an Address to search in Google Maps API:")

    # Button to Trigger Geocoding
    if st.button("CHECK MY ROOF", on_click=st.session_state.clear):
        data = getRoof_json()
        st.write('via json', data) #log

        building_insights_data = building_insights()
        st.write('building_insights', building_insights_data )
                                    

