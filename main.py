from tasks.task_robot_work_items import TaskRobotWorkItems
from tasks.task_news_data_extraction import TaskNewsDataExtraction

from util.error_manager import ErrorManager


# Tasks
ROBOT_WORK_ITEMS = "Robot Work Items"
NEWS_DATA_EXTRACTION = "News Data Extraction"

# General Constants
INSTANCE = "Instance"
RESULTS = "Results"


if __name__ == "__main__":
    tasks = {
        ROBOT_WORK_ITEMS: {
            INSTANCE: None,
            RESULTS: None,
        },
        NEWS_DATA_EXTRACTION: {
            INSTANCE: None,
            RESULTS: None,
        },
    }

    for task, task_information in tasks.items():
        try:
            instance = None

            if task == ROBOT_WORK_ITEMS:
                instance = TaskRobotWorkItems()
            elif task == NEWS_DATA_EXTRACTION:
                input_data = tasks[ROBOT_WORK_ITEMS][RESULTS]
                instance = TaskNewsDataExtraction(input_data)

            instance.execute_task()
            task_information.update(
                {INSTANCE: instance, RESULTS: instance.results}
            )
        except ErrorManager as error:
            print(error.get_error_description())
