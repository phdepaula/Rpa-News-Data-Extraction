from tasks.task_robot_work_items import TaskRobotWorkItems

from util.error_manager import ErrorManager


if __name__ == "__main__":
    tasks = [TaskRobotWorkItems]

    for task in tasks:
        instance = task()
        try:
            instance.execute_task()

            result = instance.results
        except ErrorManager as error:
            print(error.get_error_description())
