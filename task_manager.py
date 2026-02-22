import json


class Task:
    """
    The class Task defines constants for an empty task list,
    a status key, and a title key.
    """
    EMPTY = "Task List is empty."
    STATUS_KEY = "is_completed"
    TITLE_KEY = "title"

    def __init__(self):
        """
        The function initializes a class instance by
        attempting to load tasks from a JSON file, falling back
        to an empty list if the file is not found or cannot be decoded.
        """
        try:
            with open("tasks.json", "r", encoding="UTF-8") as f:
                self._tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._tasks = []

    def is_task_empty(self):
        """
        This Python function checks if a task list is empty
        by comparing its length to zero.
        :return: The `is_task_empty` method is returning a boolean value
        indicating whether the `_tasks`
        list is empty or not. If the length of the `_tasks` list is equal to 0,
        then it will return `True`,
        indicating that the list is empty. Otherwise, it will return `False`,
        indicating that the list is not empty.
        """
        return len(self._tasks) == 0

    def is_valid_index(self, index):
        """
        The function `is_valid_index` checks if a given index is within the
        valid range for a list of tasks.

        :param index: The `index` parameter is the index value that you want
        to check for validity within
        the `_tasks` list. The `is_valid_index` method checks if the `index`
        is within the valid range of indices for the `_tasks` list
        :return: a boolean value indicating whether the index is valid or not.
        It returns True if the index
        is greater than or equal to 0 and less than the length of the tasks list,
        otherwise it returns False.
        """
        return 0 <= index < len(self._tasks)

    def get_number(self):
        """
        The function `get_number` takes user input for a number,
        validates it against a condition, and returns the index if valid.
        :return: The `index` variable is being returned.
        """
        try:
            index = int(input("Enter the Number: ")) - 1
            if self.is_valid_index(index) is not True:
                raise IndexError
            return index
        except (ValueError, IndexError):
            print("Please Enter Valid Serial Number.")

    def add_task(self):
        """
        This function adds a new task with a title and default
        status of not completed to a list of tasks.
        """
        title = input("Title: ").strip()
        if title:
            is_completed = False
            self._tasks.append({self.TITLE_KEY: title, self.STATUS_KEY: is_completed})
        else:
            print("Please Enter valid title.")

    def view_task(self):
        """
        This function displays tasks with their status (completed or not) in a numbered list.
        """
        if self.is_task_empty():
            print(self.EMPTY)
        else:
            for serial, task in enumerate(self._tasks, 1):
                if task[self.STATUS_KEY]:
                    print(f"{serial}: [X] {task[self.TITLE_KEY]}")
                else:
                    print(f"{serial}: [ ] {task[self.TITLE_KEY]}")

    def update_task(self):
        """
        This function updates the status of a task in a task list based on user input.
        :return: If the user's choice is not "Y" (case insensitive),
        the function will return without making any updates to the task.
        """
        if self.is_task_empty():
            print(self.EMPTY)
        else:
            choice = input("Want to update the task Y or N: ")
            if choice.lower() != "y":
                return
            index = self.get_number()
            self._tasks[index][self.STATUS_KEY] = not self._tasks[index][
                self.STATUS_KEY
            ]

    def delete_task(self):
        """
        This function allows the user to delete a task from a list of
        tasks based on user input and task completion status.
        :return: If the user's choice is not 'Y' (case-insensitive),
        the function will return without performing any further actions.
        """
        if self.is_task_empty():
            print(self.EMPTY)
        else:
            choice = input("Want to delete the task Y or N: ")
            if choice.lower() != "y":
                return
            index = self.get_number()
            if self._tasks[index][self.STATUS_KEY]:
                print(f"{self._tasks[index]['title']} task is deleted.")
                self._tasks.pop(index)
            else:
                print(f"{self._tasks[index]['title']} task is not completed.")

    def save_task(self):
        """
        The `save_task` function saves tasks stored in a dictionary
        to a JSON file named "tasks.json" with proper indentation.
        """
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self._tasks, f, indent=2)


def show_options():
    """
    The `show_options` function displays a menu of task-related options for the user to choose from.
    """
    print("1. Add Task")
    print("2. View Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")


OPTIONS = ["1", "2", "3", "4", "5"]


def main():
    """
    The main function allows the user to interact with a Task object by choosing options to add, view,
    update, delete tasks, and save tasks.
    """
    t1 = Task()
    while True:
        show_options()

        choice = input()
        if choice not in OPTIONS:
            print("Enter Valid Options")
            continue

        match choice:
            case "1":
                t1.add_task()
            case "2":
                t1.view_task()
            case "3":
                t1.update_task()
            case "4":
                t1.delete_task()
            case "5":
                t1.save_task()
                break


if __name__ == "__main__":
    main()
