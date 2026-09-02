import json
from pathlib import Path

import pytest
import requests

from src import backend


@pytest.fixture(autouse=True)
def _chdir_with_data_dir(tmp_path, monkeypatch):
    """backend.py reads/writes relative paths like 'data/coordinates.json'."""
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)


@pytest.fixture(autouse=True)
def _mock_streamlit(monkeypatch):
    calls = {"error": [], "warning": [], "write": []}
    monkeypatch.setattr(backend.st, "error", lambda msg: calls["error"].append(msg))
    monkeypatch.setattr(backend.st, "warning", lambda msg: calls["warning"].append(msg))
    monkeypatch.setattr(backend.st, "write", lambda *args: calls["write"].append(args))
    monkeypatch.setattr(backend.st, "selectbox", lambda *args, **kwargs: 0)
    return calls


def test_getRoof_api_without_key_shows_error(monkeypatch, _mock_streamlit):
    monkeypatch.setattr(backend, "GOOGLE_MAPS_API_KEY", None)

    result = backend.getRoof_api("123 Main St")

    assert result == {}
    assert _mock_streamlit["error"]


def test_getRoof_api_network_failure(monkeypatch, _mock_streamlit):
    monkeypatch.setattr(backend, "GOOGLE_MAPS_API_KEY", "fake-key")

    def raise_connection_error(*args, **kwargs):
        raise requests.ConnectionError("boom")

    monkeypatch.setattr(backend.requests, "get", raise_connection_error)

    result = backend.getRoof_api("123 Main St")

    assert result == {}
    assert _mock_streamlit["error"]


def test_getRoof_api_non_ok_status_does_not_write_cache(monkeypatch, _mock_streamlit):
    monkeypatch.setattr(backend, "GOOGLE_MAPS_API_KEY", "fake-key")

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"status": "ZERO_RESULTS"}

    monkeypatch.setattr(backend.requests, "get", lambda *a, **k: FakeResponse())

    result = backend.getRoof_api("nowhere")

    assert result == {"status": "ZERO_RESULTS"}
    assert _mock_streamlit["error"]
    assert not Path("data/coordinates.json").exists()


def test_getRoof_api_success_writes_cache(monkeypatch, _mock_streamlit):
    monkeypatch.setattr(backend, "GOOGLE_MAPS_API_KEY", "fake-key")
    payload = {
        "status": "OK",
        "results": [{"geometry": {"location": {"lat": 1.0, "lng": 2.0}}, "formatted_address": "x", "types": []}],
    }

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return payload

    monkeypatch.setattr(backend.requests, "get", lambda *a, **k: FakeResponse())

    result = backend.getRoof_api("123 Main St")

    assert result == payload
    with open("data/coordinates.json") as f:
        assert json.load(f) == payload


def test_getRoof_json_missing_file(_mock_streamlit):
    result = backend.getRoof_json()

    assert result == {}
    assert _mock_streamlit["error"]


def test_getRoof_json_invalid_json(_mock_streamlit):
    with open("data/coordinates.json", "w") as f:
        f.write("not json")

    result = backend.getRoof_json()

    assert result == {}
    assert _mock_streamlit["error"]


def test_getRoof_json_displays_lat_lng(_mock_streamlit):
    payload = {
        "status": "OK",
        "results": [{"geometry": {"location": {"lat": 1.0, "lng": 2.0}}, "formatted_address": "x", "types": []}],
    }
    with open("data/coordinates.json", "w") as f:
        json.dump(payload, f)

    result = backend.getRoof_json()

    assert result == payload
    assert any("Latitude" in str(call[0]) for call in _mock_streamlit["write"])


def test_fetch_building_insights_without_key(monkeypatch, _mock_streamlit):
    monkeypatch.setattr(backend, "GOOGLE_MAPS_API_KEY", None)

    result = backend.fetch_building_insights(1.0, 2.0)

    assert result == {}
    assert _mock_streamlit["error"]


def test_fetch_building_insights_success_writes_cache(monkeypatch, _mock_streamlit):
    monkeypatch.setattr(backend, "GOOGLE_MAPS_API_KEY", "fake-key")
    payload = {"regionCode": "US", "solarPotential": {"maxArrayPanelsCount": 10}}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return payload

    monkeypatch.setattr(backend.requests, "get", lambda *a, **k: FakeResponse())

    result = backend.fetch_building_insights(1.0, 2.0)

    assert result == payload
    with open("data/building_insights.json") as f:
        assert json.load(f) == payload


def test_load_building_insights_cache_missing_file(_mock_streamlit):
    result = backend.load_building_insights_cache()

    assert result == {}
    assert _mock_streamlit["error"]


def test_render_building_insights_no_solar_potential(_mock_streamlit):
    backend.render_building_insights({})

    assert _mock_streamlit["error"]


def test_render_building_insights_no_financial_analyses(_mock_streamlit):
    backend.render_building_insights({"solarPotential": {"maxArrayPanelsCount": 5}})

    assert _mock_streamlit["warning"]


def test_render_building_insights_happy_path(_mock_streamlit):
    data = {
        "regionCode": "US",
        "solarPotential": {
            "maxArrayPanelsCount": 10,
            "solarPanelConfigs": [{"panelsCount": 4, "yearlyEnergyDcKwh": 1000.0}],
            "financialAnalyses": [
                {"panelConfigIndex": -1, "monthlyBill": {"currencyCode": "USD", "units": "20"}},
                {
                    "panelConfigIndex": 0,
                    "monthlyBill": {"currencyCode": "USD", "units": "100"},
                    "cashPurchaseSavings": {
                        "upfrontCost": {"currencyCode": "USD", "units": "5000"},
                        "paybackYears": 8,
                        "savings": {"savingsYear20": {"currencyCode": "USD", "units": "3000"}},
                    },
                },
            ],
        },
    }

    backend.render_building_insights(data)

    written = [str(call) for call in _mock_streamlit["write"]]
    assert any("Recommended panel count" in w for w in written)
    assert any("Upfront cost" in w for w in written)
