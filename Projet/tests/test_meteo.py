import pytest
from meteo import obtenir_meteo

def test_obtenir_meteo():
    data = obtenir_meteo("Paris")
    assert data is not None
    assert "main" in data
