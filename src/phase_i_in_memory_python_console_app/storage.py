import json
import os
from typing import List, Optional, Dict, Any
from .models import Task


class TaskStorage:
    """
    Persistent storage for tasks using file-based storage.
    """

    def __init__(self, filename: str = "tasks.json"):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
        self._filename = filename
        self.load_from_file()

    def load_from_file(self):
        """
        Load tasks from the JSON file.
        """
        if os.path.exists(self._filename):
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._tasks = {}
                    tasks_data = data.get("tasks", {})
                    for task_id_str, task_data in tasks_data.items():
                        task_id = int(task_id_str)
                        task = Task(
                            id=task_data["id"],
                            title=task_data["title"],
                            description=task_data.get("description"),
                            completed=task_data.get("completed", False)
                        )
                        self._tasks[task_id] = task

                    self._next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, KeyError, ValueError):
                # If there's an error loading the file, start fresh
                self._tasks = {}
                self._next_id = 1

    def save_to_file(self):
        """
        Save tasks to the JSON file.
        """
        data = {
            "tasks": {},
            "next_id": self._next_id
        }

        for task_id, task in self._tasks.items():
            data["tasks"][str(task_id)] = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }

        try:
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError:
            # If we can't save, we'll continue operating in memory
            pass

    def add_task(self, title: str, description: Optional[str] = None) -> int:
        """
        Add a new task to storage.

        Args:
            title: The task title (required)
            description: The task description (optional)

        Returns:
            The ID of the newly created task
        """
        task_id = self._next_id
        task = Task(id=task_id, title=title, description=description, completed=False)
        self._tasks[task_id] = task
        self._next_id += 1
        self.save_to_file()  # Save after each operation
        return task_id

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in storage.

        Returns:
            A list of all Task objects
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if the task was updated, False if task doesn't exist
        """
        if task_id not in self._tasks:
            return False

        task = self._tasks[task_id]
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        self.save_to_file()  # Save after update
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if task doesn't exist
        """
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        self.save_to_file()  # Save after deletion
        return True

    def toggle_task_status(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if task doesn't exist
        """
        if task_id not in self._tasks:
            return False

        task = self._tasks[task_id]
        task.completed = not task.completed
        self.save_to_file()  # Save after toggle
        return True

    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            The next ID that will be assigned to a new task
        """
        return self._next_id