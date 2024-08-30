from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement

from util.error_manager import ErrorManager


class SeleniumHandler:
    """
    Responsible for making Selenium resources available
    for use.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.browser = Selenium()

    def click_element(self, element: WebElement) -> None:
        """
        Method responsible for clicking in one element.
        """
        try:
            if element.is_displayed():
                element.click()
        except Exception as error:
            message = f"Error clicking in element: {error}"
            error_code = 2

            raise ErrorManager(message, error_code)

    def close_browser(self) -> None:
        """
        Method responsible for closing the browser.
        """
        try:
            self.browser.close_browser()
        except Exception as error:
            message = f"Error closing browser: {error}"
            error_code = 3

            raise ErrorManager(message, error_code)

    def find_element(self, path: str) -> WebElement:
        """
        Method responsible for finding an element.
        """
        try:
            element = self.browser.find_element(path)

            return element
        except Exception as error:
            message = f"Error finding element: {error}"
            error_code = 4

            raise ErrorManager(message, error_code)

    def input_text(self, path: str, text: str) -> None:
        """
        Method responsible for inputing text in
        a element.
        """
        try:
            self.browser.input_text(path, text)
        except Exception as error:
            message = f"Error inputing text: {error}"
            error_code = 5

            raise ErrorManager(message, error_code)

    def open_browser(self) -> None:
        """
        Method responsible for opening the browser
        and accessing the provided URL
        """
        try:
            self.browser.open_available_browser(self.url)
        except Exception as error:
            message = f"Error opening browser: {error}"
            error_code = 6

            raise ErrorManager(message, error_code)
