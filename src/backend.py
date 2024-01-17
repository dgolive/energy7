import json,sys
import streamlit as st
import logging
import pandas as pd 
import requests

with open('.env') as f:
    GOOGLE_MAPS_API_KEY = f.read()

    # if st.button("CHECK MY ROOF", on_click=st.session_state.clear):
    #     else:
    #         st.error("Invalid Address or Geocoding API Key")

def getRoof_api():
    # Perform Geocoding
    geocoding_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(geocoding_api_url)
    data = response.json()
    st.write('via API', data) #log
    # Save Coordinates into JSON file for save spent with API during tests
    with open('data/coordinates.json', 'w') as outfile:
        json.dump(data, outfile)

def getRoof_json():      
    with open('data/coordinates.json') as json_file:
        data = json.load(json_file)

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        st.write(f"Latitude: {lat}")
        st.write(f"Longitude: {lng}")
        # lat = -23.5036317
        # lng = -46.7378421

        # df_root = pd.DataFrame(data)
        # df_root[['results']] #column fmt
        
        df_roof=pd.json_normalize(
            data['results']
        )[['formatted_address','types']]

        st.write('Panda Dataframe', df_roof)

    return data
    # df1 = pd.DataFrame(data)


def building_insights():
    with open('data/building_insights.json') as json_file:
        solar_api_url_building_insights_data_json = json.load(json_file)

    st.write("Solar Building Insights Data:")
    st.write(solar_api_url_building_insights_data_json)
    st.write(solar_api_url_building_insights_data_json['regionCode'])          

    options = ("100,00", "150,00")
    index = st.selectbox("SELECT YOUR AVERAGE MONTHLY ELECTRIC BILL", range(len(options)), format_func=lambda x: options[x])
    st.write("option selected:", options[index])

    maxArrayPanelsCount = solar_api_url_building_insights_data_json['solarPotential']['maxArrayPanelsCount']
    st.write('Max Array Panels Count: ', maxArrayPanelsCount)
        
