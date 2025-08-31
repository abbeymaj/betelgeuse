# Importing packages
import logging
import os
from datetime import datetime


# Creating the logs directory for the project
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

# Creating the log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Joining the logs directory to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Overriding the basicConfig of the logging module to include the new 
# logging format
logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)