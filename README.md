# Väderappen 

En flask-app som visar nuvarande väder och tre dagars prognos för fem svenska städer.
Väderdata från [Open-Meteo.com](https://open-meteo.com/) (CC BY 4.0).

## Installation

```
git clone https://github.com/Beengt08/vaderapp.git
cd vaderapp
python -m venv venv
venv\Scripts\activate
pip install -r requirements-dev.txt
```

På Mac/Linux aktiveras miljön med `source venv/bin/activate`.

## Kör appen

```
python app.py
```

Öppna sedan http://127.0.0.1:5000 i webbläsaren.

## Köra tester och kodkontroll

```
pytest
ruff check .
ruff format --check .
```

## Projektstruktur

| Fil | Ansvar |
|---|---|
| `app.py` | Routes, statuskoder och val av mall |
| `cities.py`| De fem städerna och uppslag av koordinater |
| `weather_api.py` | Alla anrop mot Open-Meteo, timeout och eget fel |
| `parsing.py`| Rena funktioner som tolkar API-svaret |
| `filters.py` | Jinja-filtret `format_temp` |
| `templates/` | Bas-mall och sidor som ärver från den |
| `tests/`| Tester med mockning, parametrize och fixtures | 

## Frågor

### 1. Varför mockar du anropen mot API:et i dina tester, och vad skulle hända om du inte gjorde det?

Vi mockar anropen mot API:et för att testerna ska inte bli långsamma, gå sönder när vädret ändras samt att utan mockning kräver testerna internet. Mockning är även en möjlighet för att kunna framkalla fel som annars är svåra att få fram som t.ex. en timeout, och kontrollerar att appen hanterar de. Alla 34 tester funkar och ger samma resultat. 


### 2. Vad gör timeout och raise_for_status(), och varför behövs de?

Timeout gör så att appen inte väntar i evigheter och vi sätter en limit på hur länge den ska köras, raise_for_status() är en funktion som behövs på grund av att requests inte själv kastar fel vid 404 eller 500 och skulle kunna tolka en felsida som väderdata. 
I `weather_api.py`fångar jag felen och gör om dem till `WeatherApiError`, och då visar `app.py`ett felmeddelande med statuskod 503 i stället för att krascha.

### 3. Hur fungerar mallarv i Jinja2? Förklara med exempel från din egna mallar.

En mallarv innebär att en bas-mall innehåller det som är gemensamt för alla sidor, och att andra mallar ärver det och bara fyller i det som skiljer sig. I `base.html` finns Bootstrap-länken, menyraden och sidfoten med källhänvisningen, samt två block av `{% block title %}` och `{% block content %}`.`forecast.html`den börjar med `{% extends "base.html" %}` vilket sen fyller `content`med stadens väder och tabellen. Detta gör det effektivt då man behöver bara göra ändringen vid ett ställe och ändringarna syns direkt på alla sidor.

### 4. Vad är en fixture, och vilken använder du?

En fixture är en funktion som förbereder något som flera tester behöver. Den markeras med `@pytest.fixture`, och pytest skickar automatisk in den i varje test som har en parameter med samma namn. Det finns två egna fixtures, `client`som skapar Flask testklienter och den anropas utan att starta en server, sen finns det `sample_response`som ger ett falsk API-svar i samma format som Open-Meteo. `monkeypatch`används även i testerna som är inbyggda fixtures för att tillfälligt byta ut funktioner.