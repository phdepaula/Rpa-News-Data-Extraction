import logging
import os

from util.error_manager import ErrorManager


class LogGenerator:
    """
    Responsible for generatin a log file in the
    output directory.
    """

    def __init__(self):
        """
        Initializes the logger configuration.
        """
        self.log_path = "output/robot.log"
        self.log_level = logging.INFO
        self.log = logging.getLogger(__name__)
        self._configure_log()

    def _configure_log(self):
        """
        Method responsible for configuring the log with the desired
        format and handlers.
        """
        try:
            if os.path.isfile(self.log_path):
                os.remove(self.log_path)

            self.log.setLevel(self.log_level)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(self.log_path)
            file_handler.setFormatter(formatter)

            self.log.addHandler(console_handler)
            self.log.addHandler(file_handler)
        except Exception as error:
            message = f"Error configuring log: {error}"
            error_code = 100

            raise ErrorManager(message, error_code)

    def generate_debug_message(self, message: str) -> None:
        """
        Generates a log message at DEBUG level.
        """
        try:
            self.log.debug(message)
        except Exception as error:
            message = f"Error generating debug message: {error}"
            error_code = 101

            raise ErrorManager(message, error_code)

    def generate_info_message(self, message: str) -> None:
        """
        Generates a log message at INFO level.
        """
        try:
            self.log.info(message)
        except Exception as error:
            message = f"Error generating info message: {error}"
            error_code = 102

            raise ErrorManager(message, error_code)

    def generate_warning_message(self, message: str) -> None:
        """
        Generates a log message at WARNING level.
        """
        try:
            self.log.warning(message)
        except Exception as error:
            message = f"Error generating warning message: {error}"
            error_code = 103

            raise ErrorManager(message, error_code)

    def generate_error_message(self, message: str) -> None:
        """
        Generates a log message at ERROR level.
        """
        try:
            self.log.error(message)
        except Exception as error:
            message = f"Error generating error message: {error}"
            error_code = 104

            raise ErrorManager(message, error_code)

    def generate_critical_message(self, message: str) -> None:
        """
        Generates a log message at CRITICAL level.
        """
        try:
            self.log.critical(message)
        except Exception as error:
            message = f"Error generating critical message: {error}"
            error_code = 105

            raise ErrorManager(message, error_code)
