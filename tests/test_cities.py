import pytest 

from cities import get_city 


# Testar funktionen get_city med olika städer och förväntade koordinater
@pytest.mark.parametrize(
    ("city", "expected"),
    [
        ("Stockholm", (59.33, 18.07)),
        ("Göteborg", (57.71, 11.97)),
        ("Malmö", (55.61, 13.00)),
        ("Umeå", (63.83, 20.26)),
        ("Kiruna", (67.86, 20.23)),
    ],
)
# Testar att get_city returnerar rätt koordinater för varje stad
def test_get_city_returns_coordinates(city, expected): 
    assert get_city(city) == expected 
    # assert gör så att testet misslyckas om get_city(city) inte är lika med expected

# Testar att get_city returnerar None för städer som inte finns i listan
@pytest.mark.parametrize(
    "city",
    [
        "Trelleborg",
        "",
        "sTockholm",
        "Malmo",
        " Stockholm",
    ],
)
def test_get_city_returns_none_for_unknown_city(city):
    assert get_city(city) is None
    
 