"""Flask-appen: routes som kopplar ihop städer, API-anrop, tolkning och mallar."""

from flask import Flask, render_template, request

from cities import CITIES, get_city
from filters import format_temp
from parsing import parse_current, parse_daily
from weather_api import WeatherApiError, fetch_forecast

app = Flask(__name__)


# Registrera filret så att mallarna kan skriva {{ värde | format_temp }}
app.add_template_filter(format_temp)


@app.route("/")
def index():
    """Startsidan med en rullgardinslista över städerna"""
    return render_template("index.html", cities=CITIES)


@app.route("/forecast")
def forecast():
    """Visar nuvarande väder och prognos för staden i ?city=..."""
    city = request.args.get("city")

    # Ingen stad angiven: klientens fel, 400 Bad Request
    if not city:
        return render_template("error.html", message="Välj en stad."), 400

    # Staden finns inte i listan: 404 Not Found
    coordinates = get_city(city)
    if coordinates is None:
        message = f"Staden '{city}' finns inte i listan."
        return render_template("error.html", message=message), 404

    # API:et svarar inte eller ger konstiga data: 503, men appen lever vidare
    try:
        data = fetch_forecast(*coordinates)
        current = parse_current(data)
        days = parse_daily(data)
    except WeatherApiError as error:
        return render_template("error.html", message=str(error)), 503

    return render_template("forecast.html", city=city, current=current, days=days)


# Egen felhantering för 404-sidor
@app.errorhandler(404)
def page_not_found(error):
    """Egen 404-sida för adresser som inte finns."""
    return render_template("error.html", message="Sidan kunde inte hittas."), 404


# Gör att appen startar när man kör appen.
if __name__ == "__main__":
    app.run(debug=True)
