from typing import Dict, List

from RPA.Robocorp.WorkItems import WorkItems

from util.error_manager import ErrorManager


class RobotHandler:
    """
    Responsible for interacting with the robot
    and obtaining input parameters.
    """

    def __init__(self, robot_keys: List) -> None:
        self.robot_keys = robot_keys
        self.work_items = WorkItems()

    def _get_input_work_item(self) -> None:
        """
        Method responsible for getting the robot's work items.
        """
        self.work_items.get_input_work_item()

    def _search_robot_work_items(self) -> Dict:
        """
        Method responsible for searching and getting
        work item values.
        """
        work_items = {}
        input_payload = self.work_items.get_work_item_payload()

        for key in self.robot_keys:
            work_items[key] = input_payload.get(key, None)

        return work_items

    def get_robot_work_items(self) -> Dict:
        """
        Method responsible for getting the value
        of all robot work items.
        """
        try:
            self._get_input_work_item()
            work_items = self._search_robot_work_items()

            return work_items
        except Exception as error:
            message = f"Error getting robot work items: {error}"
            error_code = 1

            raise ErrorManager(message, error_code)
