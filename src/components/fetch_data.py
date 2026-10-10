# Importing packages
import sys
import requests
import numpy as np
from random import randint
from time import sleep
from bs4 import BeautifulSoup as bs
from src.components.config_entity import SourceDataURL
from src.exception import CustomException

# Creating a class to fetch data from the AAVSO website
class FetchData():
    '''
    This class fetches the magnitude data from the AAVSO website. The
    class has one method - fetch_data.
    '''
    # Creating the constructor for the class
    def __init__(self):
        '''
        This is the constructor for the FetchData class. The constructor
        instantiates the SourceDataURL class.
        '''
        self.source_data_url = SourceDataURL()
    
    # Creating a method to fetch the data from the AAVSO website
    def fetch_photometric_data(
        self,
        star: str, 
        from_jd: float, 
        to_jd: float, 
        delimiter: str = "|"
        ) -> str:
        '''
        This helper function fetches the photometric data for a given star from the AAVSO 
        website.
        ====================================================================================
        ---------------
        Parameters:
        ---------------
        star : str -> This is the name of the star for which the photometric data is to be 
        fetched. The Star identifier must be as AAVSO/VSX recognizes it, e.g. "alf Ori" 
        for Betelgeuse.
        from_jd : float -> This is the starting Julian date for the data fetch.
        to_jd : float -> This is the ending Julian date for the data fetch.
        delimiter : str -> This is the delimiter used in the fetched data. Default is "|".
        
        ---------------
        Returns:
        ---------------
        data : str -> This is the photometric data fetched from the AAVSO website as a 
        string.
        ====================================================================================
        '''
        try:
            # Defining the path
            VSX_API_URL = SourceDataURL.url
            
            # Defining the parameters for the API request
            params = {
            "view": "api.delim",
            "ident": star,
            "fromjd": from_jd,
            "tojd": to_jd,
            "delimiter": delimiter
            }
            
            # Defining the header for the API request
            # A descriptive UA is good practice when hitting a research org's API
            headers = {
                "User-Agent": "aavso-photometry-client/1.0 (research use)"
                }
            
            # Fetching the data from the AAVSO API
            resp = requests.get(VSX_API_URL, params=params, headers=headers, timeout=30)
            resp.raise_for_status()
            txt = resp.text
            
            return txt
        
        except Exception as e:
            raise CustomException(e, sys)