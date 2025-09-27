# Importing packages
import sqlite3
import pytest
from src.components.fetch_data import FetchData
from src.components.transform_data import TransformData
from src.components.config_entity import DataBaseConfig
from src.components.load_data import LoadData

# Verifying that the connection is available with the database
def test_connect_to_database():
    db_path = DataBaseConfig().db_path
    conn = sqlite3.connect(db_path)
    assert conn is not None

# verifying that data can be retrieved from the database
def test_retrieve_data_from_database():
    db_path = DataBaseConfig().db_path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lnd_alf_ori")
    data = cursor.fetchall()
    assert data is not None

# Verifying that the data can be loaded into the database
def test_load_data_into_database():
    fetch = FetchData()
    cols, rows = fetch.fetch_data()
    transform = TransformData(rows=rows, cols=cols)
    df = transform.transform_data()
    load = LoadData()
    load.load_data(df=df)