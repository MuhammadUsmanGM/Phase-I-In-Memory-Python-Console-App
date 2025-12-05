from typing import List, Optional, Dict
from .models import Task


class TaskStorage:
    """
    In-memory storage for tasks using a dictionary for O(1) access.
    """
    
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
    
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
        return True
    
    def get_next_id(self) -> int:
        """
        Get the next available task ID.
        
        Returns:
            The next ID that will be assigned to a new task
        """
        return self._next_id