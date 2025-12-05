from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a todo task with id, title, description, and completion status.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """
        Validate the task attributes after initialization.
        """
        # Validate title length (1-200 characters)
        if not (1 <= len(self.title) <= 200):
            raise ValueError("Title must be between 1 and 200 characters")
        
        # Validate description length (max 1000 characters)
        if self.description and len(self.description) > 1000:
            raise ValueError("Description must be at most 1000 characters")

    def __str__(self) -> str:
        """
        String representation of the task for display purposes.
        """
        status = "✓" if self.completed else "○"
        desc = f" - {self.description}" if self.description else ""
        return f"[{status}] {self.id}: {self.title}{desc}"