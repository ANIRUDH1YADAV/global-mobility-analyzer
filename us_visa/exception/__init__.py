import sys
from us_visa.logger import logger


def error_message_detail(error: Exception, error_detail: sys) -> str:
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return (
        f"Error in script: [{file_name}] "
        f"at line [{line_number}] — {str(error)}"
    )


class USvisaException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
        logger.error(self.error_message)

    def __str__(self) -> str:
        return self.error_message