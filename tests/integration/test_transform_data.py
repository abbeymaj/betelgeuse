# Importing packages
import pytest
import pandas as pd
from src.components.fetch_data import FetchData
from src.components.transform_data import TransformData

# Verifying that live AAVSO data can be fetched and transformed end to end
@pytest.mark.integration
def test_transform_live_data_from_aavso():
    txt = FetchData().fetch_photometric_data("alf Ori", 2458800.0, 2458830.0)
    df = TransformData(rows=[], cols=[]).to_dataframe(txt)
    assert df.shape[0] > 0
    assert df.columns.to_list() == ["Date", "Magnitude"]
    assert pd.api.types.is_numeric_dtype(df["Magnitude"])
