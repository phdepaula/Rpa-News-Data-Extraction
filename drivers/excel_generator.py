from typing import List

from RPA.Excel.Files import Files

from util.error_manager import ErrorManager


class ExcelGenerator:
    """
    Class responsible for generating excel
    files.
    """

    def __init__(self) -> None:
        self.file = Files()

    def add_data(self, data: List) -> None:
        """
        Method responsible for adding
        data inside the excel file.
        """
        try:
            self.file.append_rows_to_worksheet(data)
        except Exception as error:
            message = f"Error adding data: {error}"
            error_code = 11

            raise ErrorManager(message, error_code)

    def create_workbook(self) -> None:
        """
        Method responsible for creating
        a workbook.
        """
        try:
            self.file.create_workbook()
        except Exception as error:
            message = f"Error creating workbook: {error}"
            error_code = 12

            raise ErrorManager(message, error_code)

    def save_workbook(self, path: str) -> None:
        """
        Method responsible for saving
        the workbook.
        """
        try:
            self.file.save_workbook(path)
        except Exception as error:
            message = f"Error creating workbook: {error}"
            error_code = 12

            raise ErrorManager(message, error_code)
