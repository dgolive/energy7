import json
import logging
import os

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = 10
GEOCODING_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
SOLAR_API_BUILDING_INSIGHTS_URL = "https://solar.googleapis.com/v1/buildingInsights:findClosest"

load_dotenv()


def _load_api_key() -> str | None:
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    if key:
        return key.strip()

    # Backward compat: some .env files in this project historically hold just
    # the raw key with no `GOOGLE_MAPS_API_KEY=` prefix.
    try:
        with open(".env") as f:
            raw = f.read().strip()
    except FileNotFoundError:
        return None
    return raw or None


GOOGLE_MAPS_API_KEY = _load_api_key()


def getRoof_api(address: str) -> dict:
    """Geocode an address via the Google Maps Geocoding API and cache the result locally
    (so repeated tests against the same address don't re-spend API credit)."""
    if not GOOGLE_MAPS_API_KEY:
        st.error("Missing Google Maps API key. Add it to your .env file (see .env-sample).")
        return {}

    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"address": address, "key": GOOGLE_MAPS_API_KEY},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        logger.exception("Geocoding request failed for address=%r", address)
        st.error(f"Could not reach the Geocoding API: {exc}")
        return {}

    if data.get("status") != "OK":
        detail = f": {data['error_message']}" if data.get("error_message") else ""
        st.error(f"Geocoding failed for '{address}': {data.get('status', 'UNKNOWN_ERROR')}{detail}")
        return data

    with open("data/coordinates.json", "w") as outfile:
        json.dump(data, outfile)

    return data


def getRoof_json() -> dict:
    """Load the last cached geocoding result from disk."""
    try:
        with open("data/coordinates.json") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("No cached roof data found yet. Run a lookup first.")
        return {}

    if data.get("status") != "OK":
        st.error(f"Cached data has status '{data.get('status', 'UNKNOWN_ERROR')}', not 'OK'.")
        return data

    location = data["results"][0]["geometry"]["location"]
    lat = location["lat"]
    lng = location["lng"]
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {lng}")

    df_roof = pd.json_normalize(data["results"])[["formatted_address", "types"]]
    st.write("Matched address", df_roof)

    return data


def fetch_building_insights(lat: float, lng: float) -> dict:
    """Call the (paid) Solar API buildingInsights endpoint for the given coordinates
    and cache the result locally."""
    if not GOOGLE_MAPS_API_KEY:
        st.error("Missing Google Maps API key. Add it to your .env file (see .env-sample).")
        return {}

    try:
        response = requests.get(
            SOLAR_API_BUILDING_INSIGHTS_URL,
            params={
                "location.latitude": lat,
                "location.longitude": lng,
                "key": GOOGLE_MAPS_API_KEY,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except requests.HTTPError as exc:
        logger.exception("Solar API buildingInsights request failed for lat=%s lng=%s", lat, lng)
        message = None
        if exc.response is not None:
            try:
                message = exc.response.json().get("error", {}).get("message")
            except ValueError:
                pass
        st.error(f"Solar API request failed: {message or exc}")
        return {}
    except requests.RequestException as exc:
        logger.exception("Solar API buildingInsights request failed for lat=%s lng=%s", lat, lng)
        st.error(f"Could not reach the Solar API: {exc}")
        return {}

    with open("data/building_insights.json", "w") as outfile:
        json.dump(data, outfile)

    return data


def load_building_insights_cache() -> dict:
    """Load the last cached building insights result from disk."""
    try:
        with open("data/building_insights.json") as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("No cached building insights data found. Run a live lookup first.")
        return {}


def _money(value: dict | None) -> str:
    if not value or "units" not in value:
        return "n/a"
    currency = value.get("currencyCode", "")
    amount = int(value.get("units", 0)) + value.get("nanos", 0) / 1e9
    return f"{currency} {amount:,.2f}"


def render_building_insights(data: dict) -> None:
    """Display building insights, using the real financialAnalyses/solarPanelConfigs
    data returned by the Solar API to size a system and estimate savings for the
    electric bill the user selects."""
    solar_potential = data.get("solarPotential")
    if not solar_potential:
        st.error("No solar potential data available for this location.")
        return

    st.write("Solar Building Insights Data:")
    st.write(f"Region: {data.get('regionCode', 'n/a')}")
    st.write("Max Array Panels Count: ", solar_potential.get("maxArrayPanelsCount"))

    panel_configs = solar_potential.get("solarPanelConfigs", [])
    financial_analyses = [
        fa
        for fa in solar_potential.get("financialAnalyses", [])
        if fa.get("panelConfigIndex", -1) >= 0
    ]
    if not financial_analyses:
        st.warning("No financial analysis data available for this roof.")
        return

    def bill_label(fa: dict) -> str:
        bill = fa["monthlyBill"]
        return f"{bill.get('currencyCode', '')} {bill.get('units', '?')}/mo"

    index = st.selectbox(
        "SELECT YOUR AVERAGE MONTHLY ELECTRIC BILL",
        range(len(financial_analyses)),
        format_func=lambda i: bill_label(financial_analyses[i]),
    )
    analysis = financial_analyses[index]

    panel_config_index = analysis["panelConfigIndex"]
    if panel_config_index < len(panel_configs):
        config = panel_configs[panel_config_index]
        st.write("Recommended panel count:", config.get("panelsCount"))
        st.write("Estimated yearly production (kWh):", round(config.get("yearlyEnergyDcKwh", 0), 1))

    cash = analysis.get("cashPurchaseSavings", {})
    if cash:
        st.write("Upfront cost:", _money(cash.get("upfrontCost")))
        st.write("Savings over 20 years:", _money(cash.get("savings", {}).get("savingsYear20")))
        payback = cash.get("paybackYears")
        if payback and payback > 0:
            st.write("Estimated payback period:", f"{payback} years")
