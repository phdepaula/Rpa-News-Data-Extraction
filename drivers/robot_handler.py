from typing import Dict, List

from RPA.Robocloud.Items import RobocloudItems

from util.error_manager import ErrorManager


class RobotHandler:
    """
    Responsible for interacting with the robot
    and obtaining input parameters.
    """

    def __init__(self, robot_keys: List) -> None:
        self.robot_keys = robot_keys

    def _get_all_robot_items(self) -> RobocloudItems:
        """
        Method responsible for getting robot itens.
        """
        return RobocloudItems()

    def _search_robot_work_items(self, robot_items: RobocloudItems) -> Dict:
        """
        Method responsible for searching and get
        work item value.
        """
        work_items = {}
        input_item = robot_items.get_input_work_item()

        for key in self.robot_keys:
            work_items[key] = input_item.payload.get(key, None)

        return work_items

    def get_robot_work_items(self) -> Dict:
        """
        Method responsible for getting the value
        of all robot work items.
        """
        try:
            robot_items = self._get_all_robot_items()
            work_items = self._search_robot_work_items(robot_items)

            return work_items
        except Exception as error:
            message = f"Error getting robot work itens: {error}"
            error_code = 1

            raise ErrorManager(message, error_code)
