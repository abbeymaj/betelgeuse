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
    def fetch_data(self):
        '''
        This method fetches the magnitude data from the AAVSO website. The method uses
        webscraping to obtain the data. 
        ==================================================================================
        ---------------
        Returns:
        ---------------
        col_ls : list -> This is a list of the column names for the magnitude data.
        row_ls : list -> This is a list of the data rows for the magnitude data.
        ==================================================================================
        '''
        try:
            # Defining the URL to fetch the data
            url = self.source_data_url.url
            
            # Defining the number of pages to scrape
            pages = np.arange(0,3,1)
            
            # Creating empty lists to store the column names and data rows
            col_ls = []
            row_ls = []
            
            # Scraping the data from the AAVSO website
            for i in pages:
                url = url+str(i)
                res = requests.get(url)
                text = res.text
                data = bs(text, 'html.parser')
                tbl = data.select('table.observations')[0]
                if i == 1:
                    cols = tbl.find('thead').find_all('th')
                    for col in cols[1:-1]:
                        col_ls.append(col.string)
                else:
                    rows = tbl.find('tbody').find_all('tr', attrs={'class': ['obs tr-even', 'obs tr-odd']})
                    for row in rows:
                        td = row.find_all('td')
                        td_row = tuple(str(tr.get_text().strip()) for tr in td[1:-1])
                        row_ls.append(td_row)
                
                # Adding a random sleeo time to avoid being blocked by the AAVSO website
                sleep(randint(3,10))
        
            return col_ls, row_ls
        
        except Exception as e:
            raise CustomException(e, sys)