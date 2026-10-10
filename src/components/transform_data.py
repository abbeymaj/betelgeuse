# Importing packages
import sys
import pandas as pd
from src.utils import jd_to_calendar_date
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
    
    # Creating a method to transform the data
    def to_dataframe(self, raw_text: str, delimiter: str = "|") -> pd.DataFrame:
        '''
        This helper function converts the raw photometric data fetched from the AAVSO 
        website into a pandas DataFrame. AAVSO's free-text fields (mainly "comment", 
        occasionally "software" or "obsName") are user-submitted and can contain the 
        delimiter character itself. So instead of a naive split, this parses each row 
        positionally: a fixed-length prefix, a fixed-length suffix (both known-safe 
        structured fields), and everything left over in the middle gets rejoined into 
        "comment", however many stray delimiters it contains.
        ====================================================================================
        ---------------
        Parameters:
        ---------------
        raw_text : str -> This is the raw photometric data as a string.
        delimiter : str -> This is the delimiter used in the raw data. Default is "|".
        
        ---------------
        Returns:
        ---------------
        df : pd.DataFrame -> This is the photometric data converted into a pandas DataFrame.
        ====================================================================================
        '''
        try:
            # Reading the raw text into individual lines, ignoring empty lines
            lines = [ln for ln in raw_text.strip("\n").split("\n") if ln.strip()]
            if not lines:
                return pd.DataFrame()

            header = lines[0].split(delimiter)
            n_cols = len(header)

            if "comment" in header:
                comment_idx = header.index("comment")
            else:
                comment_idx = None

            rows = []
            bad_lines = 0
            for line in lines[1:]:
                tokens = line.split(delimiter)

                if len(tokens) == n_cols:
                    rows.append(tokens)
                elif len(tokens) > n_cols and comment_idx is not None:
                    # Merge the excess tokens back into "comment", wherever it sits.
                    excess = len(tokens) - n_cols
                    prefix = tokens[:comment_idx]
                    merged_comment = delimiter.join(tokens[comment_idx: comment_idx + 1 + excess])
                    suffix = tokens[comment_idx + 1 + excess:]
                    rows.append(prefix + [merged_comment] + suffix)
                else:
                    # Fields missing (rare) -- pad so the row does not break the DataFrame,
                    # but flag it so it's easy to spot-check afterward.
                    bad_lines += 1
                    padded = tokens + [""] * (n_cols - len(tokens))
                    rows.append(padded[:n_cols])

            if bad_lines:
                print(f"Warning: {bad_lines} row(s) had fewer fields than expected and were padded.")

            df = pd.DataFrame(rows, columns=header)

            # Numeric columns worth coercing; anything absent in a given pull is skipped.
            numeric_cols = ["JD", "mag", "uncert", "airmass", "cmag", "kmag"]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            
            # Convert AAVSO's Julian Date to a normal UTC timestamp for convenience.
            if "JD" in df.columns:
                df["datetime_utc"] = pd.to_datetime(df["JD"] - 2440587.5, unit="D", origin="unix")
                df["Date"] = df["JD"].apply(jd_to_calendar_date)
            
            # Keeping only the visual band observations
            if "band" in df.columns:
                df = df[df["band"] == "Vis."].reset_index(drop=True)

            # Renaming the mag column to Magnitude for consistency
            if "mag" in df.columns:
                df.rename(columns={"mag": "Magnitude"}, inplace=True)
            
            # Keeping the Date and Magnitude columns only
            df = df[["Date", "Magnitude"]]

            return df
        
        except Exception as e:
            raise CustomException(e, sys)
    