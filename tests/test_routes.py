import pytest

from weather_api import WeatherApiError


# Testar att startsidan visas med städerna i rullgardinslistan
def test_index_shows_cities(client):
    response = client.get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Stockholm" in html
    assert "Kiruna" in html


# Testar ett lyckat anrop med mockat API-svar
def test_forecast_shows_weather(client, monkeypatch, sample_response):
    # Byt ut fetch_forecast i app-modulen så att inget nätverk används
    monkeypatch.setattr("app.fetch_forecast", lambda lat, lon: sample_response)
    # En funktion som alltid returnerar fixturens data

    response = client.get("/forecast?city=Stockholm")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Stockholm" in html
    assert "6,0 °C" in html  # filtret har formaterat högsta temperaturen


# Testar att fel inmatning ger rätt statuskod och felsida


@pytest.mark.parametrize(
    ("url", "status"),
    [
        ("/forecast?city=Paris", 404),  # Stad som inte finns i listan
        ("/forecast", 400),  # Ingen stad angiven
        ("/sidan-finns-inte", 404),  # Okänd adress
    ],
)
def test_bad_requests_giv_error_page(client, url, status):
    response = client.get(url)
    assert response.status_code == status
    assert "alert-danger" in response.get_data(as_text=True)


# Testar att appen visar ett felmeddelande när API:et inte svarar
def test_forecast_handles_api_error(client, monkeypatch):
    def fake_fetch(lat, lon):
        raise WeatherApiError("Kunde inte hämta väderdata just nu")

    # byter ut funktionen, så att inget nätverk används
    monkeypatch.setattr("app.fetch_forecast", fake_fetch)

    response = client.get("/forecast?city=Stockholm")
    assert response.status_code == 503
    assert "Kunde inte hämta väderdata just nu" in response.get_data(as_text=True)
