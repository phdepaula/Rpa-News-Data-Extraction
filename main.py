from drivers.log_generator import LogGenerator
from tasks.task_excel_report_generator import TaskExcelReportGenerator
from tasks.task_news_data_extraction import TaskNewsDataExtraction
from tasks.task_robot_work_items import TaskRobotWorkItems

from util.error_manager import ErrorManager

# Tasks
ROBOT_WORK_ITEMS = "Robot Work Items"
NEWS_DATA_EXTRACTION = "News Data Extraction"
EXCEL_REPORT_GENERATOR = "Excel Report Generator"

# General Constants
INSTANCE = "Instance"
RESULTS = "Results"


if __name__ == "__main__":
    log = LogGenerator()
    log.generate_warning_message("Initializing process.\n")

    tasks = {
        ROBOT_WORK_ITEMS: {
            INSTANCE: None,
            RESULTS: None,
        },
        NEWS_DATA_EXTRACTION: {
            INSTANCE: None,
            RESULTS: None,
        },
        EXCEL_REPORT_GENERATOR: {
            INSTANCE: None,
            RESULTS: None,
        },
    }

    for task, task_information in tasks.items():
        try:
            log.generate_info_message(f"Task started: {task}.")
            instance = None

            if task == ROBOT_WORK_ITEMS:
                instance = TaskRobotWorkItems()
            elif task == NEWS_DATA_EXTRACTION:
                input_data = tasks[ROBOT_WORK_ITEMS][RESULTS]
                instance = TaskNewsDataExtraction(input_data)
            elif task == EXCEL_REPORT_GENERATOR:
                robot_data = tasks[ROBOT_WORK_ITEMS][RESULTS]
                news_data = tasks[NEWS_DATA_EXTRACTION][RESULTS]
                instance = TaskExcelReportGenerator(robot_data, news_data)

            instance.execute_task()

            log.generate_info_message(f"Task ended: {task}.")

            task_results = instance.get_results()
            task_information.update(
                {INSTANCE: instance, RESULTS: task_results}
            )

            log.generate_info_message(f"Task results: {task_results}\n")
        except ErrorManager as error_manager:
            log.generate_error_message(
                f"{error_manager.get_error_description()}\n"
            )
        except Exception as error:
            log.generate_error_message(f"Error: {error}\n")

    log.generate_info_message(f"Process result: {tasks}\n")
    log.generate_warning_message("Process closed.")
