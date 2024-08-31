from abc import ABC, abstractmethod
from typing import Dict


class Task(ABC):
    """
    Abstract class for executing tasks.
    """

    def __init__(self) -> None:
        self.__results = {}

    @abstractmethod
    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """

    def get_results(self) -> Dict:
        """
        Method responsible getting all results.
        """
        return self.__results

    def _update_results(self, results: Dict) -> None:
        self.__results.update(results)
