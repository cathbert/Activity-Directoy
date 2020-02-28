import logging
import os
from datetime import datetime


# Creating my logger engine class based on logging module
class LoggerEngine:
    def __init__(self):

        # The following if statement will aid in creating log files directory if it doesnt exist.
        if not os.path.exists("log files"):
            os.mkdir("log files")

        # Initializing and configuring log file
        LOG_FORMAT = "%(levelname)s - %(asctime)s %(message)s"
        if not os.path.exists(f"log files/{datetime.now().date()}.log"):
            logging.basicConfig(filename=os.path.join("log files", f"{datetime.now().date()}.log"),
                                level=logging.DEBUG,
                                format=LOG_FORMAT,
                                filemode="a")
        else:
            logging.basicConfig(filename=os.path.join("log files", f"{datetime.now().date()}.log"),
                                level=logging.DEBUG,
                                format=LOG_FORMAT,
                                filemode="a")

        self.logger = logging.getLogger()

    # method to log in a WARNING
    def log_warning(self, message):
        self.logger.warning(message)

    # method to log in INFO
    def log_info(self, message):
        self.logger.info(message)

    # method to log in an ERROR
    def log_error(self, message):
        self.logger.error(message)

    # method to log in a DEBUG
    def log_debug(self, message):
        self.logger.debug(message)

    # method to log in a CRITICAL
    def log_critical(self, message):
        self.logger.critical(message)

    # method to log user logout
    def log_user_logout(self, message):
        self.logger.info(message)
