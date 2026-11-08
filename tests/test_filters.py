import pytest

from filters import format_temp


# Testar avrundning, noll, minusgrader och saknade värden
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (12.34, "12,3 °C"),  # Avrundas till decimal
        (0, "0,0 °C"),  # Noll ska inte bli tomt
        (-5.0, "-5,0 °C"),  # Minusgrader ska visas korrekt
        (None, "-"),  # Saknat värden ger streck
    ],
)
def test_format_temp(value, expected):  # Testar format_temp med olika typer av värden
    assert format_temp(value) == expected
