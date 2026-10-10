# Importing packages
import os
from dataclasses import dataclass

# Creating a class to store the path to the database
@dataclass
class DataBaseConfig():
    '''
    This class stores the path to the database.
    '''
    db_path:str = os.path.join('db', 'alpha_orionis.db')

# Creating a class to store the source data url
@dataclass
class SourceDataURL():
    '''
    This class stores the source data URL. Fetches photometry observations for 
    Betelgeuse (alf Ori) from the AAVSO International Database (AID) via the VSX delimited-text API.
    '''
    url: str = 'https://www.aavso.org/vsx/index.php'