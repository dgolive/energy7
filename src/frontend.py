import streamlit as st

from src.backend import (
    fetch_building_insights,
    getRoof_api,
    getRoof_json,
    load_building_insights_cache,
    render_building_insights,
)


def mainpage():
    st.sidebar.markdown("### Menu")

    # Streamlit App Title
    st.title("Solar 7 - Help the Climate Change")
    st.markdown('an Open Source Project')

    # Input Address
    address = st.text_input("Enter an Address to search in Google Maps API:")
    use_cache = st.checkbox(
        "Use cached data (skip live API calls)",
        help="Reuse the last saved lookup instead of spending Geocoding/Solar API credit.",
    )

    # Button to Trigger Geocoding
    if st.button("CHECK MY ROOF"):
        if use_cache:
            geocode_data = getRoof_json()
        else:
            if not address:
                st.error("Please enter an address first.")
                return
            geocode_data = getRoof_api(address)
            if geocode_data.get("status") == "OK":
                getRoof_json()

        if geocode_data.get("status") != "OK":
            return

        if use_cache:
            insights_data = load_building_insights_cache()
        else:
            location = geocode_data["results"][0]["geometry"]["location"]
            insights_data = fetch_building_insights(location["lat"], location["lng"])

        if insights_data:
            render_building_insights(insights_data)
