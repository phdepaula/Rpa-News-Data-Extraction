from drivers.robot_handler import RobotHandler
from tasks.task import Task

from util.error_manager import ErrorManager


class TaskRobotWorkItems(Task):
    """
    Task to get Robot Work Items.
    """

    def __init__(self) -> None:
        self.robot_keys = ["search_phrase", "sort_by"]

    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """
        try:
            robot_handler = RobotHandler(self.robot_keys)
            work_items = robot_handler.get_robot_work_items()

            self._update_results(work_items)
        except ErrorManager as error_manager:
            raise error_manager
        except Exception as error:
            message = f"Error executing task Robot Work Items: {error}"
            error_code = 20

            raise ErrorManager(message, error_code)
