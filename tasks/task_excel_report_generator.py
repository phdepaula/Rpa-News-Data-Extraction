from datetime import datetime
from typing import Dict

from drivers.excel_generator import ExcelGenerator
from tasks.task import Task

from util.error_manager import ErrorManager


class TaskExcelReportGenerator(Task):
    """
    Task to generate the excel report
    """

    SEARCH_PHRASE = "search_phrase"
    TITLE = "title"
    DESCRIPTION = "description"
    DATE = "date"
    IMAGE_SRC = "image_src"

    def __init__(self, input_data: Dict) -> None:
        super().__init__()
        self.input_data = input_data
        self.excel_generator = ExcelGenerator()

    def _create_template(self) -> None:
        """
        Method responsible for creating the
        excel file.
        """
        self.excel_generator.create_workbook()

        columns = [
            [
                "Title",
                "Date",
                "Description",
                "Picture Filename",
                "Count of Search Phrase",
                "Title and Description Have Money?",
            ]
        ]
        self.excel_generator.add_data(columns)

    def _save_file(self) -> None:
        """
        Method responsible for saving the excel file.
        """
        current_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        path = f"output/report_news_{current_date}.xlsx"
        self.excel_generator.save_workbook(path)

    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """
        try:
            self._create_template()
            self._save_file()
        except ErrorManager as error_manager:
            raise error_manager
        except Exception as error:
            message = f"Error executing task News Data Extraction: {error}"
            error_code = 40

            raise ErrorManager(message, error_code)
