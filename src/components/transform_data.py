# Importing packages
import sys
import pandas as pd
from src.utils import extract_date
from src.exception import CustomException


# Creating a class to transform the data fetched from the AAVSO website
class TransformData():
    '''
    This class transforms the data that is scraped from the AAVSO website
    and prepares the data to be loaded into the database. The class 
    contains three methods - the constructor, a method to convert the calendar 
    date to a datetime format and the transform_data method.
    '''
    # Creating the constructor for the class
    def __init__(self, rows:list, cols:list):
        '''
        This is the constructor for the class. It has two arguments - the 
        row and columns returned from the FetchData class.
        '''
        self.rows = rows
        self.cols = cols
    
    # Creating a method to convert the calendar date to a datetime format
    def convert_calendar_date_to_datetime(self, df:pd.DataFrame):
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
            df['Date'] = df['Calendar_Date'].apply(lambda x: extract_date(x))

            # Covnerting the Date feature into a DateTime feature
            df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)

            # Sorting the dataframe by the Date feature and dropping duplicates
            df = df.sort_values(by='Date').drop_duplicates(['Date'], keep='last')

            return df
        
        except Exception as e:
            raise CustomException(e, sys)
    
    
    # Creating a method to transform the data
    def transform_data(self):
        '''
        This method cleans the data and prepares the data to be loaded into the 
        landing layer.
        ================================================================================
        ---------------
        Returns:
        ---------------
        df : pandas dataframe -> This is returns a pandas dataframe with clean data.
        ================================================================================
        '''
        try:
            # Creating a dataframe with the rows and columns
            df = pd.DataFrame(self.rows, columns=self.cols)
            
            # Creating the Adjusted Magnitude feature
            df['Magnitude'] = pd.to_numeric(df['Magnitude'], errors='coerce')

            # Renaming the Calendar Date feature to Calendar_Date
            df = df.rename(columns={'Calendar Date': 'Calendar_Date'})

            # Extracting the date feature and converting it to a datetime object
            df = self.convert_calendar_date_to_datetime(df).astype(str)

            # Taking the Date and Adjusted Magnitude features and creating a new dataframe
            sub_df = df[['Date', 'Magnitude']]

            return sub_df
            
        except Exception as e:
            raise CustomException(e, sys)
    