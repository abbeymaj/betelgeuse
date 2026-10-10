# Importing packages
import pandas as pd
from datetime import datetime, timedelta, timezone
from src.utils import get_julian_date
from src.components.fetch_data import FetchData
from src.components.transform_data import TransformData
from src.components.load_data import LoadData

# Defining the star and the number of days of history to fetch on each run
STAR = "alf Ori"
LOOKBACK_DAYS = 60

# Running the pipeline to load the data into the database
if __name__ == '__main__':

    # Defining the Julian date window for the data fetch
    now = datetime.now(timezone.utc)
    from_jd = get_julian_date(now - timedelta(days=LOOKBACK_DAYS))
    to_jd = get_julian_date(now)

    # Fetching the data from the AAVSO API
    data = FetchData()
    raw_text = data.fetch_photometric_data(star=STAR, from_jd=from_jd, to_jd=to_jd)

    # Transforming the data before loading
    transform = TransformData(rows=[], cols=[])
    df = transform.to_dataframe(raw_text)

    # Loading the transformed data into the database table
    load = LoadData()
    load.load_data(df=df)
