# Importing packages
import pytest
from src.components.fetch_data import FetchData

# Verifying that photometric data can be fetched from the live AAVSO API
@pytest.mark.integration
def test_fetch_live_data_from_aavso():
    txt = FetchData().fetch_photometric_data("alf Ori", 2458800.0, 2458830.0)
    header = txt.strip("\n").split("\n")[0].split("|")
    assert "JD" in header
    assert "mag" in header
    assert len(txt.strip("\n").split("\n")) > 1
