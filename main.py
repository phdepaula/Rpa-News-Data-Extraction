from tasks.task_robot_work_items import TaskRobotWorkItems

if __name__ == "__main__":
    tasks = [TaskRobotWorkItems]

    for task in tasks:
        instance = task()
        instance.execute_task()

        result = instance.results
        print(result)