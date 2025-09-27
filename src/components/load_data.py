# Importing packages
import sys
import sqlite3
import pandas as pd
from src.components.config_entity import DataBaseConfig
from src.exception import CustomException

# Creating a class to load the data into the SQLite database
class LoadData():
    '''
    This class loads the data, which has been scraped from the AAVSO website,
    into a landing layer within the sqlite database. The class has two methods -
    the constructor and the load_data method.
    '''
    # Creating the constructor for the class
    def __init__(self):
        '''
        This is the constructor for the LoadData class. The constructor 
        instantiates the path to the database.
        '''
        self.db = DataBaseConfig()
        
    # Creating the method to load the data into the database
    def load_data(self, df:pd.DataFrame):
        '''
        This method loads the data into the database.
        ================================================================================
        ---------------
        Parameters:
        ---------------
        df : pandas DataFrame -> This is a pandas dataframe with the scraped data.
        
        ---------------
        Returns:
        ---------------
        None
        ================================================================================
        '''
        try:
            # Creating a connection to the database
            conn = sqlite3.connect(self.db.db_path)
            
            # Creating the cursor object
            cursor = conn.cursor() 
            
            # Inserting the data into the database
            for _, row in df.iterrows():
                cursor.execute(
                    '''
                    INSERT INTO lnd_alf_ori (Date, Magnitude)
                    VALUES (
                    ?,
                    ?
                    )
                    ON CONFLICT (Date) DO UPDATE SET
                    Magnitude = excluded.Magnitude
                    WHERE true
                    ''', 
                    (row['Date'], row['Magnitude'])
                )
            
            # Committing the changes to the database
            conn.commit()
            
            # Closing the connection to the database
            conn.close()
        
        except Exception as e:
            raise CustomException(e, sys)