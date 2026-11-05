"""Alla anrop mot Open-Meteo API hanteras här"""

import requests

URL = "https://api.open-meteo.com/v1/forecast"  # Bas-URL för Open-Meteo API:et
TIMEOUT = 5  # Timeout för HTTP-anrop i sekunder


class WeatherApiError(Exception):
    """Kastas när väderdata inte kan hämtas eller tolkas"""


def fetch_forecast(latitude, longitude):
    """Hämtar nuvarande väder och tre dagars prognos för en plats.

    Returnerar API-Svaret som en ordbok
    Kastar WeatherApiError om anropet misslyckas eller svaret inte är JSON"""

    params = {  # Parametrar för API-anropet
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    }
    # Försök att göra API-anropet och tolka svaret
    try:
        response = requests.get(URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        raise WeatherApiError(
            "Kunde inte hämta väderdata just nu, vänligen försök igen senare"
        ) from error
    except ValueError as error:
        raise WeatherApiError("Väderdata kom i ett oväntat format") from error
