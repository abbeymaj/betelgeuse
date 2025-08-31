# Import packages
import sys

# Creating a function to fetch the error message from the sys module
def fetch_error_message(error, error_detail:sys):
    '''
    This function fetches the error information from the sys module.
    ====================================================================
    ------------------
    Parameters:
    ------------------
    error - str : This is the error message.
    error_detail: This is the error detail from the sys module.
    
    ------------------
    Returns:
    ------------------
    error_message - This is the error message from the sys module.
    =====================================================================
    '''
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno
    error_message = f"Error occurred in script name [{file_name}], line_number [{line_no}], with error message [{str(error)}]"
    return error_message

# Creating a custom class to display exceptions thrown by the system.
# This custom class will inherit from the Python Exception class.
class CustomException(Exception):
    '''
    The CustomException class is a custom class to display system exceptions. 
    This class inherits from the Python Exception class.
    The class contains two methods - The constructor and a method to display the error message.
    '''
    # Defining the constructor for the class
    def __init__(self, error_message, error_detail:sys):
        '''
        This is the constructor for the CustomException class.
        The constructor takes two arguments - The error message and the error detail.
        '''
        super().__init__(error_message)
        self.error_message = fetch_error_message(error_message, error_detail=error_detail)
    
    # Defining the method to display the error message
    def __str__(self):
        '''
        This method displays the error message.
        '''
        return self.error_message