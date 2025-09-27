# Importing packages
import pytest
import pandas as pd
from src.utils import extract_date
from src.components.fetch_data import FetchData
from src.components.transform_data import TransformData

# Creating a module to return the transformed dataframe
@pytest.fixture(scope='module')
def create_transformed_df():
    fetch = FetchData()
    col_ls, row_ls = fetch.fetch_data()
    transform = TransformData(rows=row_ls, cols=col_ls)
    df_transformed = transform.transform_data()
    return df_transformed

# Verifying that the transformed dataset is not empty
def test_transformed_dataset_not_null(create_transformed_df):
    df = create_transformed_df
    assert df is not None

# Verifying that the transformed dataset is a pandas dataframe
def test_transformed_dataset_is_dataframe(create_transformed_df):
    df = create_transformed_df
    assert isinstance(df, pd.DataFrame)

# Verifying that the transformed dataset has rows
def test_transformed_dataset_has_rows(create_transformed_df):
    df = create_transformed_df
    assert df.shape[0] > 0

# Verifying that the transformed dataset has columns
def test_transformed_dataset_has_columns(create_transformed_df):
    df = create_transformed_df
    assert df.shape[1] > 0

# Verifying that the transformed dataset has the correct columns
def test_transformed_dataframe_columns_match(create_transformed_df):
    df = create_transformed_df
    assert df.columns.to_list() == ['Date', 'Magnitude']