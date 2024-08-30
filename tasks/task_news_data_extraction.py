import time

from drivers.selenium_handler import SeleniumHandler
from tasks.task import Task

from util.error_manager import ErrorManager


class TaskNewsDataExtraction(Task):
    """
    Task to extract news data from the
    website informed..
    """

    def __init__(self) -> None:
        self.url = "https://apnews.com/"
        self.selenium_handler = SeleniumHandler(self.url)

    def _close_browser(self) -> None:
        """
        Method responsible for closing browser.
        """
        self.selenium_handler.close_browser()

    def _open_browser(self) -> None:
        """
        Method responsible for opening browser.
        """
        self.selenium_handler.open_browser()

    def _searching_phrase(self) -> None:
        """
        Method responsible for searching phrase.
        """

    def _selecting_search_bar(self) -> None:
        """
        Method responsible for selecting
        the search bar.
        """
        loupe_header_path = (
            """//*[@id="Page-header-trending-zephr"]"""
            + """/div[2]/div[3]/bsp-search-overlay/button"""
        )
        loupe_header_element = self.selenium_handler.find_element(
            loupe_header_path
        )
        self.selenium_handler.click_element(loupe_header_element)

    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """
        try:
            self._open_browser()
            self._selecting_search_bar()

            time.sleep(2)

            self.close_browser()
        except ErrorManager as error_manager:
            raise error_manager
        except Exception as error:
            message = f"Error executing task News Data Extraction: {error}"
            error_code = 11

            raise ErrorManager(message, error_code)
