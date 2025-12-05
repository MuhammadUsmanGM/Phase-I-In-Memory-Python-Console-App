"""
Agent Skill Implementation for Todo Management
This module provides programmatic access to todo management functions
that can be used by AI agents.
"""

from typing import List, Optional, Dict, Any
from src.phase_i_in_memory_python_console_app.storage import TaskStorage
from src.phase_i_in_memory_python_console_app.models import Task


class TodoAgentSkill:
    """
    Agent skill implementation for todo management that provides programmatic
    access to todo operations for AI agents.
    """

    def __init__(self, filename: str = "tasks.json"):
        self.storage = TaskStorage(filename)

    def add_task(self, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Adds a new task to the todo list.

        Args:
            title: The task title (1-200 characters)
            description: The task description (max 1000 characters)

        Returns:
            Dictionary with 'success' boolean and 'task_id' if successful
        """
        try:
            task_id = self.storage.add_task(title, description)
            return {
                "success": True,
                "task_id": task_id,
                "message": f"Task added successfully with ID: {task_id}"
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

    def view_tasks(self) -> Dict[str, Any]:
        """
        Retrieves all tasks from the todo list.

        Returns:
            Dictionary with 'success' boolean and 'tasks' list
        """
        try:
            tasks = self.storage.get_all_tasks()
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                })

            return {
                "success": True,
                "tasks": task_list
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Updates an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            Dictionary with 'success' boolean and message
        """
        try:
            success = self.storage.update_task(task_id, title, description)
            if success:
                return {
                    "success": True,
                    "message": f"Task with ID {task_id} updated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Deletes a task from the todo list.

        Args:
            task_id: The ID of the task to delete

        Returns:
            Dictionary with 'success' boolean and message
        """
        try:
            success = self.storage.delete_task(task_id)
            if success:
                return {
                    "success": True,
                    "message": f"Task with ID {task_id} has been deleted"
                }
            else:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def mark_task_complete(self, task_id: int) -> Dict[str, Any]:
        """
        Toggles the completion status of a task.

        Args:
            task_id: The ID of the task to mark

        Returns:
            Dictionary with 'success' boolean and message
        """
        try:
            task = self.storage.get_task(task_id)
            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found"
                }

            success = self.storage.toggle_task_status(task_id)
            if success:
                status = "complete" if task.completed else "pending"
                return {
                    "success": True,
                    "message": f"Task with ID {task_id} marked as {status}"
                }
            else:
                return {
                    "success": False,
                    "error": f"Could not toggle status for task with ID {task_id}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_task(self, task_id: int) -> Dict[str, Any]:
        """
        Retrieves a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Dictionary with 'success' boolean and task details
        """
        try:
            task = self.storage.get_task(task_id)
            if task:
                return {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Convenience function to create a skill instance
def create_skill(filename: str = "tasks.json") -> TodoAgentSkill:
    """
    Creates and returns a new instance of the TodoAgentSkill.
    """
    return TodoAgentSkill(filename)