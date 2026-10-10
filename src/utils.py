# Importing packages
import sys
import io
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
from datetime import datetime
from src.components.config_entity import SourceDataURL
from src.exception import CustomException 

# Creating a helper function to transform magnitude data to numeric
def magnitude_to_numeric(df:pd.DataFrame):
    '''
    This function takes the Magnitude feature and adjusts it for any errors, using the
    Error feature.
    ====================================================================================
    ---------------
    Parameters:
    ---------------
    df : pandas dataframe -> This is the pandas dataframe with the Magnitude feature.
    
    ---------------
    Returns:
    ---------------
    df : pandas dataframe -> This is the pandas dataframe with the Adjusted Magnitude
    feature.
    ====================================================================================
    
    '''
    try:
        # Converting the Magnitude and Error features into a numeric feature
        df['Magnitude'] = pd.to_numeric(df['Magnitude'], errors='coerce')
        return df
    
    except Exception as e:
        raise CustomException(e, sys)

# Creating a helper function to extract the date feature
def get_julian_date(date: datetime) -> float:
    '''
    This function extracts the date from the Calendar Date feature from the 
    data scraped from the AAVSO website.
    ====================================================================================
    ---------------
    Parameters:
    ---------------
    date : datetime -> This is the date that is received from the API.
    
    ---------------
    Returns:
    ---------------
    Julian date : float -> This the Julian date converted from the UCT Datetime.
    ====================================================================================
    '''
    try:
        jd = date.toordinal() + 1721424.5
        jd += (date.hour + date.minute / 60 + date.second / 3600) / 24
        return jd
    
    except Exception as e:
        raise CustomException(e, sys)

# Creating a helper function to convert the julian date to a calendar date
def jd_to_calendar_date(jd:float):
    '''
    This helper function converts a Julian date to a calendar date, formatted to
    "YYYY-MM-DD". 
    ====================================================================================
    ---------------
    Parameters:
    ---------------
    jd : float -> This is the Julian date that needs to be converted.
    
    ---------------
    Returns:
    ---------------
    date : datetime -> This is the calendar date converted from the Julian date.
    ====================================================================================
    '''
    try:
        dt = pd.to_datetime(jd - 2440587.5, unit="D", origin="unix")
        return dt.strftime("%Y-%m-%d")
    
    except Exception as e:
        raise CustomException(e, sys)


# Creating the helper function to convert the photometry data into a dataframe
