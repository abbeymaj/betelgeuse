# Importing packages
import pandas as pd
from src.components.fetch_data import FetchData 
from src.components.transform_data import TransformData
from src.components.load_data import LoadData 

# Running the pipeline to load the data into the database
if __name__ == '__main__':
    
    # Fetching the data from the AAVSO website
    data = FetchData()
    cols, rows = data.fetch_data()
    
    # Transforming the data before loading
    transform = TransformData(rows=rows, cols=cols)
    df = transform.transform_data()
    
    # Loading the transformed data into the database table
    load = LoadData()
    load.load_data(df=df)