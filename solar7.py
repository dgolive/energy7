import json,sys
import streamlit as st
import requests
import logging

with open('.env') as f:
    GOOGLE_MAPS_API_KEY = f.read()

# logging.basicConfig(filename='solar7.log')
# logging.debug('This message should go to the log file')

st.sidebar.markdown("### Menu")

# Streamlit App Title
st.title("Solar 7 - Help the Climate Change")
st.markdown('an Open Source Project')

# Input for Address
address = st.text_input("Enter an Address to search in Google Maps API:")

# Button to Trigger Geocoding
if st.button("CHECK MY ROOF"):
    ## Perform Geocoding
    geocoding_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(geocoding_api_url)
    data = response.json()

    ## Save Coordinates into JSON file for save spent with API during tests
    # with open('data/coordinates.json', 'w') as outfile:
    #     json.dump(data, outfile)

    # with open('data/coordinates.json') as json_file:
    #     data = json.load(json_file)

    st.write('via api', data) #log

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']

        st.write(f"Latitude: {lat}")
        st.write(f"Longitude: {lng}")

        # lat = -23.5036317
        # lng = -46.7378421

        # Button to Trigger Solar API   
        
        # solar_api_url_building_insights = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lng}&requiredQuality=HIGH&key={GOOGLE_MAPS_API_KEY}"
        # st.write({solar_api_url_building_insights})  # URL Logging
        # solar_api_url_building_insights_response = requests.get(solar_api_url_building_insights)
        # solar_api_url_building_insights_data = solar_api_url_building_insights_response.json()
        
        ## Save Coordinates into JSON file for save spent with API during tests
        # with open('data/building_insights.json', 'w') as outfile:
        #     json.dump(solar_api_url_building_insights_data, outfile)

        with open('data/building_insights.json') as json_file:
            solar_api_url_building_insights_data_json = json.load(json_file)

        st.write("Solar Building Insights Data:")
        st.write(solar_api_url_building_insights_data_json)

        #YOUR AVERAGE MONTHLY ELECTRIC BILL
        # Based on your usage, Project Sunroof can recommend the optimal solar installation size that can fit on your roof.
        # If you don’t know your monthly bill, make your best guess.

        option = st.selectbox(
            'YOUR AVERAGE MONTHLY ELECTRIC BILL',
            ('R$ 100,00', 'R$ 200,00'))

        st.write('You selected:', option)


        # Your recommended solar installation size
        # Our recommendation is based on your bill, electricity rates in your area, and the sunlight your roof receives.

        # Based on Google’s database of aerial imagery and maps, Project Sunroof knows how much space on your roof can fit solar panels and where is best to install them.

        # Solar panel installations sizes are measured in kilowatts (kW).

        # We recommend an installation less than 100% of your electrical usage because, in most areas, there is no financial benefit to producing more power than you can consume. Sizing below 100% provides a buffer in case your electricity consumption decreases over time.


        maxArrayPanelsCount = solar_api_url_building_insights_data_json['solarPotential']['maxArrayPanelsCount']
        st.write('Max Array Panels Count: ', maxArrayPanelsCount)

        # "solarPotential":{
        # "maxArrayPanelsCount":24



        # Para instalações solares, installationSize se refere à saída de kW em vez da área ou contagem de painéis
        # installationSize = panelsCount * panelCapacityWatts/1000 kW


    else:
        st.error("Invalid Address or Geocoding API Key")


