import json,sys
import streamlit as st
import logging

with open('.env') as f:
    GOOGLE_MAPS_API_KEY = f.read()

    # if st.button("CHECK MY ROOF", on_click=st.session_state.clear):
    #     else:
    #         st.error("Invalid Address or Geocoding API Key")

def getRoof():
    # Button to Trigger Geocoding
    st.button("CHECK MY ROOF", on_click=st.session_state.clear)
       ## Perform Geocoding
       # geocoding_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
       # response = requests.get(geocoding_api_url)
       # data = response.json()
       # st.write('via API', data) #log
       ## Save Coordinates into JSON file for save spent with API during tests
       # with open('data/coordinates.json', 'w') as outfile:
       #     json.dump(data, outfile)
    with open('data/coordinates.json') as json_file:
        data = json.load(json_file)
    st.write('via json', data) #log
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        st.write(f"Latitude: {lat}")
        st.write(f"Longitude: {lng}")
        # lat = -23.5036317
        # lng = -46.7378421
        
        ## Query by Google Maps API
        # solar_api_url_building_insights = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lng}&requiredQuality=HIGH&key={GOOGLE_MAPS_API_KEY}"
        # st.write({solar_api_url_building_insights})  # URL Logging
        # solar_api_url_building_insights_response = requests.get(solar_api_url_building_insights)
        # solar_api_url_building_insights_data = solar_api_url_building_insights_response.json()
        ## Save Coordinates into JSON file for save spent with API during tests
        # with open('data/building_insights.json', 'w') as outfile:
        #     json.dump(solar_api_url_building_insights_data, outfile)
        
        ## Open JSON files
        with open('data/building_insights.json') as json_file:
            solar_api_url_building_insights_data_json = json.load(json_file)
        st.write("Solar Building Insights Data:")
        st.write(solar_api_url_building_insights_data_json)
        st.write(solar_api_url_building_insights_data_json['regionCode'])          
            
        """
        # YOUR AVERAGE MONTHLY ELECTRIC BILL
        Based on your usage, Project Sunroof can recommend the optimal solar installation size that can fit on your roof.
        If you don’t know your monthly bill, make your best guess.
        """
        
        options = ("100,00", "150,00")
        index = st.selectbox("SELECT YOUR AVERAGE MONTHLY ELECTRIC BILL", range(len(options)), format_func=lambda x: options[x])
        st.write("option selected:", options[index])
        """
        Your recommended solar installation size
        Our recommendation is based on your bill, electricity rates in your area, and the sunlight your roof receives.
        Based on Google’s database of aerial imagery and maps, Project Sunroof knows how much space on your roof can fit solar panels and where is best to install them.
        Solar panel installations sizes are measured in kilowatts (kW).
        We recommend an installation less than 100% of your electrical usage because, in most areas, there is no financial benefit to producing more power than you can consume. Sizing below 100% provides a buffer in case your electricity consumption decreases over time.
        """
        
        maxArrayPanelsCount = solar_api_url_building_insights_data_json['solarPotential']['maxArrayPanelsCount']
        st.write('Max Array Panels Count: ', maxArrayPanelsCount)
        
        
        """
        "solarPotential":{
        "maxArrayPanelsCount":24
        Para instalações solares, installationSize se refere à saída de kW em vez da área ou contagem de painéis
        installationSize = panelsCount * panelCapacityWatts/1000 kW
        Consumo anual de energia doméstica
        Como mencionado anteriormente, a API Solar determina o consumo mensal de eletricidade com base no valor da conta mensal e no custo da eletricidade em que uma casa está localizada. Depois de determinar o consumo mensal de eletricidade de uma casa, calculamos o consumo anual de energia em KWh usando a seguinte fórmula:
        monthlyKWhEnergyConsumption = st.text_input("Enter with your Montly Energy Consuption in KWh: ")
        annualKWhEnergyConsumption = monthlyKWhEnergyConsumption * 12
        st.write(annualKWhEnergyConsumption)
        Produção anual de energia solar
        A API Solar estima a produção anual de energia de uma instalação solar considerando fatores como a intensidade da luz solar, o ângulo da luz solar e o número de horas de luz solar utilizável que uma região recebe anualmente.
        As instalações solares produzem eletricidade de corrente contínua (CC), que precisa ser convertida em eletricidade de corrente alternada (CA) por um inversor para que possa ser usada em casa. Parte da eletricidade é perdida durante o processo de conversão, e a eficiência do inversor determina quanto é perdido.
        A eficiência do processo de conversão é chamada de dedução de CC para CA. Para compensar a perda, a API Solar multiplica a produção anual da instalação solar por uma redução de CC para CA de 0,85. O resultado é a produção anual de eletricidade CA, conforme mostrado na seguinte fórmula:
        initialAcKwhPerYear = yearlyEnergyDcKwh * 0.85
        """
        

