import sys
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from log import logging

def get_error_message_detail(error, error_detail: sys):
    """
    Creates a detailed error message including the file and line number.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in Python script name [{file_name}] line number [{line_number}] with error message: [{str(error)}]"
    
    return error_message


class CustomException(Exception):
    """
    Custom exception class for the application.
    
    When an error occurs, it formats a detailed message using the
    get_error_message_detail function and logs it.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = get_error_message_detail(error_message, error_detail=error_detail)
        logging.error(self.error_message)
    
    def __str__(self):
        return self.error_message