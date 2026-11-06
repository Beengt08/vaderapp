import pytest

from parsing import parse_current, parse_daily
from weather_api import WeatherApiError


# Testar att temperatur och vind plockas ut ur ett gilltig svar
def test_parse_current_returns_value(sample_response):
    assert parse_current(sample_response) == {"temperature": 5.1, "wind_speed": 12.6}


def test_parse_daily_returns_one_dict_per_day(sample_response):
    days = parse_daily(sample_response)
    assert len(days) == 3
    assert days[0] == {
        "date": "2026-11-06",
        "max": 6.0,
        "min": 2.4,
        "precipitation": 0.0,
    }


# Testar att saknad, tom eller ofullständig prognos ger WeatherApiError
@pytest.mark.parametrize(
    "data",
    [
        None,  # Saknad prognos
        {},  # Tomt svar
        {"current": {}},  # "current" finns men det är tom
    ],
)
def test_parse_current_raises_on_bad_data(data):
    with pytest.raises(WeatherApiError):
        parse_current(data)


# Testar att saknad, tom eller ofullständig daglig prognos ger WeatherApiError
@pytest.mark.parametrize(
    "data",
    [
        None,  # Saknad prognos
        {},  # "Daily" saknas
        {"daily": {"time": ["2026-11-06"]}},  # tre av fyra listor saknas
        {
            "daily": {
                "time": [],
                "temperature_2m_max": [],
                "temperature_2m_min": [],
                "precipitation_sum": [],
            }
        },  # alla listor är tomma
        {
            "daily": {
                "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
                "temperature_2m_max": [6.0, 4.6],
                "temperature_2m_min": [2.4, 2.0, 1.2],
                "precipitation_sum": [0.0, 0.0, 0.0],
            }
        },  # Olika långa listor: bara två maxtemperaturer
    ],
    ids=["none", "daily-saknas", "nycklar-saknas", "tomma-listor", "olika-langd"],
)
def test_parse_daily_raises_on_bad_data(data):
    with pytest.raises(WeatherApiError):
        parse_daily(data)
