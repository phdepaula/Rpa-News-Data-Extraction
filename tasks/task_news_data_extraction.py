import time
from typing import Dict

from drivers.selenium_handler import SeleniumHandler
from tasks.task import Task

from util.error_manager import ErrorManager


class TaskNewsDataExtraction(Task):
    """
    Task to extract news data from the
    website informed.
    """

    SEARCH_PHRASE = "search_phrase"
    SORT_BY = "sort_by"
    TITLE = "title"
    DESCRIPTION = "description"
    DATE = "date"
    IMAGE_SRC = "image_src"

    def __init__(self, input_data: Dict) -> None:
        super().__init__()
        self.input_data = input_data
        self.__url = "https://www.aljazeera.com/"
        self.__selenium_handler = SeleniumHandler(self.__url)

    def _close_browser(self) -> None:
        """
        Method responsible for closing browser.
        """
        self.__selenium_handler.close_browser()

    def _get_articles_information(self) -> None:
        """
        Method responsible for getting information
        from all articles.
        """
        articles_path = (
            """//*[@id="main-content-area"]/div[2]/div[2]/article"""
        )
        articles_elements = self.__selenium_handler.find_elements(
            articles_path
        )
        quantity_articles = len(articles_elements)

        position = 1

        while position <= quantity_articles:
            title_path = (
                articles_path + f"[{position}]/div[2]/div[1]/h3/a/span"
            )
            title_text = self.__selenium_handler.get_element_text(title_path)

            description_path = (
                articles_path + f"[{position}]/div[2]/div[2]/div/p"
            )
            description_text = self.__selenium_handler.get_element_text(
                description_path
            )

            date_path = (
                articles_path
                + f"[{position}]/div[2]/footer/div/div/div/div/span[2]"
            )
            date_text = self.__selenium_handler.get_element_text(date_path)

            image_path = articles_path + f"[{position}]/div[3]/div/div/img"
            attribute = "src"
            image_src = self.__selenium_handler.get_element_attribute(
                image_path, attribute
            )

            self._update_results(
                {
                    str(position): {
                        self.TITLE: title_text,
                        self.DESCRIPTION: description_text,
                        self.DATE: date_text,
                        self.IMAGE_SRC: image_src,
                    }
                }
            )

            position += 1

    def _open_browser(self) -> None:
        """
        Method responsible for opening browser.
        """
        self.__selenium_handler.open_browser()

    def _open_search_bar(self) -> None:
        """
        Method responsible for opening
        the search bar.
        """
        loupe_path = (
            """//*[@id="root"]/div/div[1]/div[1]/div/"""
            + """header/div[4]/div[2]/button"""
        )
        loupe_element = self.__selenium_handler.find_element(loupe_path)
        self.__selenium_handler.click_element(loupe_element)

    def _searching_phrase(self, search_phrase: str) -> None:
        """
        Method responsible for searching phrase.
        """
        text_bar_path = (
            """//*[@id="root"]/div/div[1]/div[2]/div/"""
            + """div/form/div[1]/input"""
        )
        self.__selenium_handler.input_text(text_bar_path, search_phrase)

        loupe_path = (
            """//*[@id="root"]/div/div[1]/div[2]/div/div"""
            + """/form/div[2]/button"""
        )
        loupe_element = self.__selenium_handler.find_element(loupe_path)
        self.__selenium_handler.click_element(loupe_element)

    def _sort_news(self) -> None:
        """
        Method responsible for sorting news
        based on value provided.
        """
        sort_by = self.input_data.get(self.SORT_BY, None)

        if sort_by is not None:
            try:
                path = """//*[@id="search-sort-option"]"""
                self.__selenium_handler.select_option(path, sort_by.lower())
            except ErrorManager as error_manager:
                print(
                    "Unable to sort news: "
                    + f"{error_manager.get_error_description()}"
                )

    def _wait_for_page_to_load(self, seconds: int) -> None:
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
            self._wait_for_page_to_load(2)
            self._open_search_bar()
            self._wait_for_page_to_load(2)

            search_phrase = self.input_data.get(self.SEARCH_PHRASE, None)

            if search_phrase is not None:
                self._searching_phrase(search_phrase)
                self._wait_for_page_to_load(2)
                self._sort_news()
                self._wait_for_page_to_load(2)
                self._get_articles_information()
                self._wait_for_page_to_load(2)
        except ErrorManager as error_manager:
            raise error_manager
        except Exception as error:
            message = f"Error executing task News Data Extraction: {error}"
            error_code = 30

            raise ErrorManager(message, error_code)
        finally:
            self._close_browser()
