import logging
import sys
import os
from logging.handlers import RotatingFileHandler
import config

class Logger:
    def __init__(self, name, log_level=None, log_file=None, log_format=None):
        self.logger = logging.getLogger(name)
        
        # Use configuration values or default values
        self.log_level = log_level or config.LOG_LEVEL
        self.log_file = log_file or config.LOG_FILE
        self.log_format = log_format or config.LOG_FORMAT
        
        # Set logging level
        self.logger.setLevel(self.log_level)
        
        # Create formatter
        formatter = logging.Formatter(self.log_format)
        
        # Setup console output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Setup file output
        if self.log_file:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            file_handler = RotatingFileHandler(
                self.log_file, maxBytes=10485760, backupCount=5
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
