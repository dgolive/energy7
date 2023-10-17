import json,sys
import streamlit as st
import requests
import logging

# logging.basicConfig(filename='solar7.log')
# logging.debug('This message should go to the log file')



# data2 = st.json(data)
# st.write(data2)

# all_widgets = st.create_widgets(data2)
# st.write(all_widgets)

# Para instalações solares, installationSize se refere à saída de kW em vez da área ou contagem de painéis
# installationSize = panelsCount * panelCapacityWatts/1000 kW

with open('data/coordinates.json') as json_file:
    data = json.load(json_file)

st.sidebar.markdown("### Map Layers")

# Streamlit App Title
st.title("Solar 7 - Help the Climate Change")
st.markdown('an Open Source Project')

# Input for Address
address = st.text_input("Enter an Address to search in Google Maps API:")

## Buttons
if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_stage(stage):
    st.session_state.stage = stage

# Button to Trigger Geocoding
if st.button("Get Coordinates", on_click=set_stage, args=(1,)):
    ## Perform Geocoding
    # geocoding_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyDquwjG9pbEcD56YGyRwmzvmbotq797F1c"
    # response = requests.get(geocoding_api_url)
    # data = response.json()
    # st.write(data) #log

    ## Save Coordinates into JSON file for save spent with API during tests
    # with open('data/coordinates.json', 'w') as outfile:
    #     json.dump(data, outfile)

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']

        st.write(f"Latitude: {lat}")
        st.write(f"Longitude: {lng}")

        # lat = -23.5036317
        # lng = -46.7378421

        # Button to Trigger Solar API   
        if st.session_state.stage > 0:
            st.button("Get Solar Building Insights Data", on_click=set_stage, args=(2,))
            solar_api_url_building_insights = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lng}&requiredQuality=HIGH&key=AIzaSyDquwjG9pbEcD56YGyRwmzvmbotq797F1c"
            st.write({solar_api_url_building_insights})  # URL Logging
            solar_api_url_building_insights_response = requests.get(solar_api_url_building_insights)
            solar_api_url_building_insights_data = solar_api_url_building_insights_response.json()
            
            st.write("Solar Building Insights Data:")
            st.write(solar_api_url_building_insights_data)

    else:
        st.error("Invalid Address or Geocoding API Key")
