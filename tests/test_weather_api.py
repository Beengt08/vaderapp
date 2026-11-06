from unittest.mock import Mock

import pytest
import requests

import weather_api
from weather_api import WeatherApiError, fetch_forecast


# En funktion som testar att fetch_forecast returnerar JSON-data korrekt
def test_fetch_forecast_returns_json(monkeypatch):

    fake_response = Mock()
    fake_response.json.return_value = {"current": {}, "daily": {}}

    fake_get = Mock(return_value=fake_response)
    monkeypatch.setattr(weather_api.requests, "get", fake_get)

    assert fetch_forecast(59.33, 18.07) == {"current": {}, "daily": {}}


# En funktion som testar att fetch_forecast hanterar olika fel korrekt
@pytest.mark.parametrize(
    ("get_error", "status_error", "json_error"),
    [
        (requests.Timeout(), None, None),  # Simulerar en timeout
        (None, requests.exceptions.HTTPError(), None),  # Simulerar ett HTTP-fel
        (None, None, ValueError()),  # Simulerar ett JSON-fel
    ],
    ids=["timeout", "http_error", "json_error"] # Namnger testfallen för tydlighet
)
def test_fetch_forecast_raises_weather_api_error(
    monkeypatch, get_error, status_error, json_error
):
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = status_error
    fake_response.json.side_effect = json_error

    fake_get = Mock(return_value=fake_response, side_effect=get_error)
    monkeypatch.setattr(weather_api.requests, "get", fake_get)

    with pytest.raises(WeatherApiError):
        fetch_forecast(59.33, 18.07)
