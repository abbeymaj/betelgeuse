# Importing packages
import sqlite3
import pytest
from src.components.fetch_data import FetchData
from src.components.transform_data import TransformData
from src.components.config_entity import DataBaseConfig
from src.components.load_data import LoadData

# Verifying that the connection is available with the database
@pytest.mark.integration
def test_connect_to_database():
    db_path = DataBaseConfig().db_path
    conn = sqlite3.connect(db_path)
    assert conn is not None

# verifying that data can be retrieved from the database
@pytest.mark.integration
def test_retrieve_data_from_database():
    db_path = DataBaseConfig().db_path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lnd_alf_ori")
    data = cursor.fetchall()
    assert data is not None

# Verifying that the data can be loaded into the database
@pytest.mark.integration
def test_load_data_into_database():
    fetch = FetchData()
    txt = fetch.fetch_photometric_data("alf Ori", 2458800.0, 2458830.0)
    transform = TransformData(rows=[], cols=[])
    df = transform.to_dataframe(txt)
    load = LoadData()
    load.load_data(df=df)