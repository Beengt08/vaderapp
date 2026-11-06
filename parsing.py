"""Rena funktioner som gör om API-svaret till enkla strukturer för mallarna"""

from weather_api import WeatherApiError


def parse_current(data):
    """Plockar ut nuvarande temperatur och vindhastighet
    Den returnerar även en ordbok med nycklarna "temperature" och "wind_speed"."""
    try:
        current = data["current"]
        temperature = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]
    except (KeyError, TypeError) as error:
        raise WeatherApiError("Väderdata för just nu saknas") from error
    return {"temperature": temperature, "wind_speed": wind_speed}


def parse_daily(data):
    """Gör om dagsprognosen till en lista med en ordbok per dag."""
    try:
        daily = data["daily"]
        dates = daily["time"]
        max_temps = daily["temperature_2m_max"]
        min_temps = daily["temperature_2m_min"]
        precipitation = daily["precipitation_sum"]
    except (KeyError, TypeError) as error:
        raise WeatherApiError("Prognosdata saknas") from error

    # Tomma listor eller olika längder betyder att svaret är ofullständigt.
    lengths_match = len(dates) == len(max_temps) == len(min_temps) == len(precipitation)
    if not dates or not lengths_match:
        raise WeatherApiError("Prognosdata är ofullständig")

    # Para ihop listorna så att varje dag blir en ordbok.
    days = []
    for date, high, low, rain in zip(dates, max_temps, min_temps, precipitation):
        days.append({"date": date, "max": high, "min": low, "precipitation": rain})
    return days
