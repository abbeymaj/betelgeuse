# Importing packages
import os
from dataclasses import dataclass

# Creating a class to store the path to the database
@dataclass
class DataBaseConfig():
    '''
    This class stores the path to the database.
    '''
    db_path:str = os.path.join('db', 'betelgeuse.db')

# Creating a class to store the source data url
@dataclass
class SourceDataURL():
    '''
    This class stores the source data URL.
    '''
    url : str = 'https://apps.aavso.org/webobs/results/?star=betelgeuse&num_results=200&page='