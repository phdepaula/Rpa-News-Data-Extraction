import re
import os
from datetime import datetime
from typing import Dict, List

from drivers.excel_generator import ExcelGenerator
from tasks.task import Task

from util.error_manager import ErrorManager
import requests


class TaskExcelReportGenerator(Task):
    """
    Task to generate the excel report
    """

    SEARCH_PHRASE = "search_phrase"
    SORT_BY = "sort_by"
    TITLE = "title"
    DESCRIPTION = "description"
    DATE = "date"
    IMAGE_SRC = "image_src"
    COLUMNS = "columns"
    OUTPUT = "output"

    def __init__(self, robot_data: Dict, news_data: Dict) -> None:
        super().__init__()
        self.robot_data = robot_data
        self.news_data = news_data
        self.__excel_generator = ExcelGenerator()
        self.__excel_path = None

    def _check_if_contains_monetary_value(self, text: str) -> bool:
        """
        Method responsible for checking whether
        the provided text contains any monetary value.

        Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
        """
        standard = (
            r"(\$\d{1,3}(,\d{3})*(\.\d{1,2})?)|"
            r"(\d{1,3}(,\d{3})*(\.\d{1,2})?\s*dollars)|"
            r"(USD\s*\d+)|"
            r"(\d+\s*USD)"
        )
        return bool(re.search(standard, text))

    def _count_number_of_occurrences(
        self, text: str, search_phrase: str
    ) -> int:
        """
        Method responsible for counting how many times the search_phrase
        appears in the text.
        """
        return text.count(search_phrase)

    def _create_template(self) -> None:
        """
        Method responsible for creating the
        excel file.
        """
        self.__excel_generator.create_workbook()

        columns = [
            [
                "Title",
                "Date",
                "Description",
                "Picture Filename",
                "Occurrence of Search Phrase in Title and Description",
                "Title and Description Have Monetary Value?",
                "News Image",
            ]
        ]
        self.__excel_generator.add_data(columns)

        self._update_results({self.COLUMNS: columns})

    def _download_image(self, url: str, name: str) -> None:
        """
        Method responsible for download an image
        to the output directory.
        """
        try:
            response = requests.get(url)

            if response.status_code == 200:
                path = f"{self.OUTPUT}/{name}.jpg"

                with open(path, "wb") as image:
                    image.write(response.content)
        except Exception:
            print(f"Failed to download image {name}.")

    def _format_excel_file(self) -> None:
        """
        Method responsible for formatting excel file.
        """
        self.__excel_generator.set_row_height(self.__excel_path, 135)
        self.__excel_generator.adjust_width_to_show_data(self.__excel_path)

    def _generate_report_data(self) -> List:
        """
        Method responsible for generating report data.
        """
        for key, data in self.news_data.items():
            title = self._treat_text(data.get(self.TITLE, ""))
            description = self._treat_text(data.get(self.DESCRIPTION, ""))
            date = self._treat_date(data.get(self.DATE, ""))
            picture_filename = data.get(self.IMAGE_SRC, "")

            combined_text = title + " " + description
            search_phrase = self.robot_data.get(self.SEARCH_PHRASE, None)

            number_of_occurrences = (
                self._count_number_of_occurrences(combined_text, search_phrase)
                if search_phrase is not None
                else 0
            )
            monetary_value = self._check_if_contains_monetary_value(
                combined_text
            )

            data_result = [
                [
                    title,
                    date,
                    description,
                    picture_filename,
                    number_of_occurrences,
                    monetary_value,
                ]
            ]

            self.__excel_generator.add_data(data_result)
            self._update_results({key: data_result})
            self._download_image(picture_filename, key)

    def _include_news_image(self) -> None:
        """
        Method responsible for including
        the news image inside the report.
        """
        for key in self.news_data.keys():
            image_path = f"{self.OUTPUT}/{key}.jpg"
            cell = f"G{int(key) + 1}"

            image_added = self.__excel_generator.add_image_to_cell(
                image_path, cell, self.__excel_path
            )

            if image_added is True:
                os.remove(image_path)

    def _save_file(self) -> None:
        """
        Method responsible for saving the excel file.
        """
        current_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.__excel_path = f"{self.OUTPUT}/report_news_{current_date}.xlsx"

        self.__excel_generator.save_workbook(self.__excel_path)

    def _treat_date(self, date: str) -> str:
        """
        Method responsible for trating date.
        Format: DD MMM AAAA
        """
        date_text = self._treat_text(date)

        standard = r"(\d{1,2}\s*[A-Za-z]{3}\s*\d{4})"
        match_standard = re.search(standard, date_text)

        if match_standard:
            date_matched = match_standard.group(1)

            try:
                new_date = datetime.strptime(date_matched, "%d %b %Y")

                return new_date.strftime("%d %b %Y")
            except ValueError:
                return date_matched

        return ""

    def _treat_text(self, text: str) -> str:
        """
        Method responsible for removing
        extra spaces.
        """
        return text.strip()

    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """
        try:
            self._create_template()
            self._generate_report_data()
            self._save_file()
            self._include_news_image()
            self._format_excel_file()
        except ErrorManager as error_manager:
            raise error_manager
        except Exception as error:
            message = f"Error executing task News Data Extraction: {error}"
            error_code = 40

            raise ErrorManager(message, error_code)
