"""Gemensamma fixtures för alla tester."""

import pytest

from app import app


@pytest.fixture  # Skapar en testklient för Flask-appen
def client():
    """Flasks testklient: anropar routes utan att starta en riktig server."""
    app.config["TESTING"] = True  # Gör att appen körs i testläge
    with app.test_client() as client:  # Låtsas vara en klient utan riktig server
        yield client  # Lämnar testklienten till testet


@pytest.fixture
def sample_response():
    """Ett giltigt API-svar i samma format som Open-Meteo, utan nätverk"""
    return {
        "current": {"temperature_2m": 5.1, "wind_speed_10m": 12.6},
        "daily": {
            "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
            "temperature_2m_max": [6.0, 4.6, 4.6],
            "temperature_2m_min": [2.4, 2.0, 1.2],
            "precipitation_sum": [0.0, 0.0, 0.0],
        },
    }
