# Importing packages
import pytest
from src.components.fetch_data import FetchData

# Verifying that the data can be fetched from the website
def test_fetch_data():
    fetch = FetchData()
    col_ls, row_ls = fetch.fetch_data()
    assert col_ls is not None
    assert row_ls is not None
    assert "Magnitude" in col_ls