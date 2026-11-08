"""Egna Jinja-filter för att visa värden snyggt i mallarna."""


def format_temp(value):
    """Formaterar en temperatur som '12,3 °C'. Returnerar '-' om värdet saknas."""

    # Om värdet saknas visar vi ett streck i stället för att krascha
    if value is None:
        return "-"

    # En decimal, svenskt decimalkomma och enhet
    return f"{value:.1f}".replace(".", ",") + " °C"
