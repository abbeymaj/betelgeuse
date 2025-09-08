# Importing packages
import sys
import pandas as pd
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
def extract_date(row):
    '''
    This function extracts the date from the Calendar Date feature from the 
    data scraped from the AAVSO website.
    ====================================================================================
    ---------------
    Parameters:
    ---------------
    df : pandas dataframe -> This is the pandas dataframe with the Calendar Date 
    feature.
    
    ---------------
    Returns:
    ---------------
    df : pandas dataframe -> This is the pandas dataframe with the extracted Date 
    feature.
    ====================================================================================
    '''
    try:
        year = row.split()[0]
        month = row.split()[1].split('.')[0]
        day = row.split()[2].split('.')[0]
        return year+'-'+month+'-'+day
    
    except Exception as e:
        raise CustomException(e, sys)

# Creating a helper function to convert the calendar date to datetime format
def convert_calendar_date_to_datetime(df:pd.DataFrame):
    '''
    This method converts the calendar date to a datetime object.
    =================================================================================
    ---------------
    Parameters:
    ---------------
    df : pandas dataframe -> This is the pandas dataframe with the date feature.
    
    ---------------
    Returns:
    ---------------
    df : pandas dataframe -> This is the pandas dataframe with the date feature
    converted to a datetime object.
    =================================================================================
    '''
    try:
        # Extracting the date from the Calendar Date feature
        df['Date'] = df['Calendar_Date'].apply(lambda x: extract_date_feature(x))

        # Covnerting the Date feature into a DateTime feature
        df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)

        # Sorting the dataframe by the Date feature and dropping duplicates
        df = df.sort_values(by='Date').drop_duplicates(['Date'], keep='last')

        return df
    
    except Exception as e:
        raise CustomException(e, sys)