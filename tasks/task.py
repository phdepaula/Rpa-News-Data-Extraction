from abc import ABC, abstractmethod
from typing import Any


class Task(ABC):
    """
    Abstract class for executing tasks.
    """

    def __init__(self) -> None:
        self.results = None

    @abstractmethod
    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """

    def _update_results(self, results: Any) -> None:
        self.results = results
