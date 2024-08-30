from drivers.robot_handler import RobotHandler
from tasks.task import Task


class TaskRobotWorkItems(Task):
    """
    Task to get Robot Work Items.
    """

    def __init__(self) -> None:
        self.robot_keys = ["search_phrase", "filter", "sort_by"]

    def execute_task(self) -> None:
        """
        Method responsible for executing task.
        """
        robot_handler = RobotHandler(self.robot_keys)
        work_items = robot_handler.get_robot_work_items()

        self._update_results(work_items)
