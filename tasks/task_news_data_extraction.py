import time
from typing import Dict

from drivers.selenium_handler import SeleniumHandler
from tasks.task import Task

from util.error_manager import ErrorManager


class TaskNewsDataExtraction(Task):
    """
    Task to extract news data from the
    website informed..
    """

    SEARCH_PHRASE = "search_phrase"
    FILTER = "filter"
    SORT_BY = "sort_by"

    def __init__(self, input_data: Dict) -> None:
        self.input_data = input_data
        self.__url = "https://apnews.com/"
        self.__selenium_handler = SeleniumHandler(self.__url)

    def _close_advertisement(self) -> None:
        """
        Method responsible for closing the advertisement
        if it appears
        """
        try:
            close_icon_path = "/html/body/div[7]/div/div/a"
            close_icon_element = self.__selenium_handler.find_element(
                close_icon_path
            )
            self.__selenium_handler.click_element(close_icon_element)
        except ErrorManager:
            print("Non-existent advertising")

    def _close_browser(self) -> None:
        """
        Method responsible for closing browser.
        """
        self.__selenium_handler.close_browser()

    def _open_browser(self) -> None:
        """
        Method responsible for opening browser.
        """
        self.__selenium_handler.open_browser()

    def _opening_search_bar(self) -> None:
        """
        Method responsible for opening
        the search bar.
        """
        loupe_path = (
            """//*[@id="Page-header-trending-zephr"]"""
            + """/div[2]/div[3]/bsp-search-overlay/button"""
        )
        loupe_element = self.__selenium_handler.find_element(loupe_path)
        self.__selenium_handler.click_element(loupe_element)

    def _searching_phrase(self) -> None:
        """
        Method responsible for searching phrase.
        """
        text_bar_path = (
            """//*[@id="Page-header-trending-zephr"]/div[2]"""
            + """/div[3]/bsp-search-overlay/div/form/label/input"""
        )
        text = self.input_data.get(self.SEARCH_PHRASE, "")
        self.__selenium_handler.input_text(text_bar_path, text)

        loupe_path = (
            """//*[@id="Page-header-trending-zephr"]/div[2]/div[3]"""
            + """/bsp-search-overlay/div/form/button"""
        )
        loupe_element = self.__selenium_handler.find_element(loupe_path)
        self.__selenium_handler.click_element(loupe_element)

    def wait_for_page_to_load(self, seconds: int) -> None:
        """
        Method responsible for waiting page to load.
        """
        time.sleep(seconds)

    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """
        try:
            self._open_browser()
            self.wait_for_page_to_load(5)
            self._close_advertisement()
            self.wait_for_page_to_load(3)
            self._opening_search_bar()
            self.wait_for_page_to_load(3)
            self._searching_phrase()
            self.wait_for_page_to_load(3)
            self._close_browser()
            self._update_results(["results"])
        except ErrorManager as error_manager:
            raise error_manager
        except Exception as error:
            message = f"Error executing task News Data Extraction: {error}"
            error_code = 11

            raise ErrorManager(message, error_code)
