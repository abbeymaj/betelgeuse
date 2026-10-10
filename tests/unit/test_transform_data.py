# Importing packages
import pytest
import pandas as pd
from src.components.transform_data import TransformData
from src.exception import CustomException

# Defining a small sample of AAVSO delimited output for the unit tests
SAMPLE_RAW = (
    "JD|mag|uncert|band|comment|obsName\n"
    "2458800.5|1.20|0.05|Vis.|clear sky|Observer A\n"
    "2458801.5|1.25|0.04|Vis.|haze|Observer B\n"
)

# Defining a sample with observations in several bands
MIXED_BAND_RAW = (
    "JD|mag|band|comment\n"
    "2458800.5|1.20|Vis.|clear\n"
    "2458800.6|0.99|V|\n"
    "2458800.7|2.80|B|\n"
    "2458800.8|-2.56|I|\n"
    "2458801.5|1.25|Vis.|haze\n"
)

# Creating a helper to build a TransformData instance
# (rows and cols are not used by to_dataframe)
def make_transform():
    return TransformData(rows=[], cols=[])

# Creating a fixture that returns the transformed sample dataframe
@pytest.fixture
def sample_df():
    return make_transform().to_dataframe(SAMPLE_RAW)

# Verifying that the transformed dataset is a pandas dataframe
@pytest.mark.unit
def test_to_dataframe_returns_dataframe(sample_df):
    assert isinstance(sample_df, pd.DataFrame)

# Verifying that only the Date and Magnitude columns are kept
@pytest.mark.unit
def test_to_dataframe_columns_match(sample_df):
    assert sample_df.columns.to_list() == ["Date", "Magnitude"]

# Verifying that one row is produced per observation
@pytest.mark.unit
def test_to_dataframe_row_count(sample_df):
    assert sample_df.shape[0] == 2

# Verifying that the Julian date is converted to a YYYY-MM-DD calendar date
@pytest.mark.unit
def test_to_dataframe_converts_jd_to_date(sample_df):
    assert sample_df["Date"].to_list() == ["2019-11-13", "2019-11-14"]

# Verifying that the magnitude is converted to a numeric type
@pytest.mark.unit
def test_to_dataframe_magnitude_is_numeric(sample_df):
    assert pd.api.types.is_numeric_dtype(sample_df["Magnitude"])
    assert sample_df["Magnitude"].to_list() == [1.20, 1.25]

# Verifying that only visual band observations are kept
@pytest.mark.unit
def test_to_dataframe_keeps_only_visual_band():
    df = make_transform().to_dataframe(MIXED_BAND_RAW)
    assert df["Magnitude"].to_list() == [1.20, 1.25]
    assert df["Date"].to_list() == ["2019-11-13", "2019-11-14"]

# Verifying that the index is contiguous after filtering out other bands
@pytest.mark.unit
def test_to_dataframe_resets_index_after_band_filter():
    df = make_transform().to_dataframe(MIXED_BAND_RAW)
    assert df.index.to_list() == [0, 1]

# Verifying that a response with no visual observations returns an empty dataframe
@pytest.mark.unit
def test_to_dataframe_no_visual_band_returns_empty_dataframe():
    raw = "JD|mag|band\n2458800.5|0.99|V\n2458800.6|2.80|B\n"
    df = make_transform().to_dataframe(raw)
    assert df.empty
    assert df.columns.to_list() == ["Date", "Magnitude"]

# Verifying that a non-numeric magnitude is coerced to NaN
@pytest.mark.unit
def test_to_dataframe_invalid_magnitude_becomes_nan():
    raw = "JD|mag|comment\n2458800.5|<2.0|fainter than\n"
    df = make_transform().to_dataframe(raw)
    assert df["Magnitude"].isna().all()

# Verifying that a delimiter inside the comment does not shift the columns
@pytest.mark.unit
def test_to_dataframe_delimiter_in_comment():
    raw = (
        "JD|mag|comment|obsName\n"
        "2458800.5|1.20|clouds | moon nearby|Observer A\n"
    )
    df = make_transform().to_dataframe(raw)
    assert df.shape[0] == 1
    assert df["Date"].iloc[0] == "2019-11-13"
    assert df["Magnitude"].iloc[0] == 1.20

# Verifying that rows with missing fields are padded rather than dropped
@pytest.mark.unit
def test_to_dataframe_pads_short_rows(capsys):
    raw = (
        "JD|mag|comment|obsName\n"
        "2458800.5|1.20|clear\n"
    )
    df = make_transform().to_dataframe(raw)
    assert df.shape[0] == 1
    assert df["Magnitude"].iloc[0] == 1.20
    assert "1 row(s) had fewer fields" in capsys.readouterr().out

# Verifying that a custom delimiter is honoured
@pytest.mark.unit
def test_to_dataframe_custom_delimiter():
    raw = "JD;mag;comment\n2458800.5;1.20;clear\n"
    df = make_transform().to_dataframe(raw, delimiter=";")
    assert df["Date"].iloc[0] == "2019-11-13"
    assert df["Magnitude"].iloc[0] == 1.20

# Verifying that blank lines in the response are ignored
@pytest.mark.unit
def test_to_dataframe_ignores_blank_lines():
    raw = "\nJD|mag\n\n2458800.5|1.20\n\n"
    df = make_transform().to_dataframe(raw)
    assert df.shape[0] == 1

# Verifying that an empty response returns an empty dataframe
@pytest.mark.unit
def test_to_dataframe_empty_input_returns_empty_dataframe():
    df = make_transform().to_dataframe("")
    assert isinstance(df, pd.DataFrame)
    assert df.empty

# Verifying that a header with no observations returns an empty dataframe
@pytest.mark.unit
def test_to_dataframe_header_only_returns_empty_dataframe():
    df = make_transform().to_dataframe("JD|mag|comment\n")
    assert df.empty
    assert df.columns.to_list() == ["Date", "Magnitude"]

# Verifying that a response without a JD column raises a CustomException
@pytest.mark.unit
def test_to_dataframe_missing_jd_raises_custom_exception():
    with pytest.raises(CustomException):
        make_transform().to_dataframe("mag|comment\n1.20|clear\n")