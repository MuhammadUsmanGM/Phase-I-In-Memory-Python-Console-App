import re
from typing import List, Tuple
from .storage import TaskStorage
from .models import Task


class TodoCLI:
    """
    Command Line Interface for the Todo application.
    Handles user input, command parsing, and output formatting.
    """
    
    def __init__(self):
        self.storage = TaskStorage()
        self.running = True
    
    def display_help(self):
        """
        Display help information with available commands.
        """
        print("\nTodo Console App")
        print("===============")
        print("Commands:")
        print("- add (a) - Add a new task")
        print("- view/list (l) - View all tasks")
        print("- update (u) - Update a task")
        print("- delete (d) - Delete a task")
        print("- complete/mark (c) - Mark task as complete/incomplete")
        print("- help - Show this help")
        print("- quit (q) - Exit application")
        print()
    
    def parse_command(self, user_input: str) -> Tuple[str, List[str]]:
        """
        Parse user input into command and arguments.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            A tuple of (command, arguments list)
        """
        # Remove extra whitespace and convert to lowercase for command
        user_input = user_input.strip()
        if not user_input:
            return "help", []
        
        # Split by spaces, but preserve quoted strings
        parts = re.split(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', user_input)
        command = parts[0].lower()
        args = [part.strip('"') for part in parts[1:]]  # Remove quotes from args
        
        return command, args
    
    def handle_add(self, args: List[str]):
        """
        Handle the add command.
        Usage: add "title" "description" or interactive input
        """
        if len(args) >= 1:
            title = args[0]
            description = args[1] if len(args) > 1 else None
        else:
            # Interactive input
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Title is required")
                return
            description_input = input("Enter task description (optional): ").strip()
            description = description_input if description_input else None
        
        try:
            task_id = self.storage.add_task(title, description)
            print(f"Task added successfully with ID: {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def handle_view(self, args: List[str]):
        """
        Handle the view/list command.
        """
        tasks = self.storage.get_all_tasks()
        
        if not tasks:
            print("\nNo tasks found")
            return
        
        print("\nID  | Status | Title              | Description")
        print("----|--------|--------------------|------------------")
        for task in tasks:
            status = "✓" if task.completed else "○"
            title = task.title[:18] + ".." if len(task.title) > 18 else task.title
            description = task.description[:16] + ".." if task.description and len(task.description) > 16 else (task.description or "")
            print(f"{task.id:<3} | {status:^6} | {title:<18} | {description}")
        print()
    
    def handle_update(self, args: List[str]):
        """
        Handle the update command.
        Usage: update id "new title" "new description" or interactive input
        """
        if not args:
            print("Usage: update <id> [new title] [new description]")
            return
        
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return
        
        # Get the current task to check if it exists
        current_task = self.storage.get_task(task_id)
        if not current_task:
            print(f"Error: Task with ID {task_id} not found")
            return
        
        # Get new title and description from arguments or interactive input
        if len(args) >= 2:
            new_title = args[1] if args[1] != "" else None
        else:
            new_title_input = input(f"Enter new title (current: {current_task.title}): ").strip()
            new_title = new_title_input if new_title_input else None
            
        if len(args) >= 3:
            new_description = args[2] if args[2] != "" else None
        else:
            desc_prompt = f"Enter new description (current: {current_task.description or 'None'}): "
            new_description_input = input(desc_prompt).strip()
            new_description = new_description_input if new_description_input else None
        
        # Update the task
        success = self.storage.update_task(task_id, new_title, new_description)
        if success:
            print(f"Task with ID {task_id} updated successfully")
        else:
            print(f"Error: Could not update task with ID {task_id}")
    
    def handle_delete(self, args: List[str]):
        """
        Handle the delete command.
        Usage: delete id or interactive input
        """
        if not args:
            task_id_input = input("Enter task ID to delete: ").strip()
            if not task_id_input:
                print("Error: Task ID is required")
                return
            try:
                task_id = int(task_id_input)
            except ValueError:
                print("Error: Task ID must be a number")
                return
        else:
            try:
                task_id = int(args[0])
            except ValueError:
                print("Error: Task ID must be a number")
                return
        
        success = self.storage.delete_task(task_id)
        if success:
            print(f"Task with ID {task_id} has been deleted")
        else:
            print(f"Error: Task with ID {task_id} not found")
    
    def handle_complete(self, args: List[str]):
        """
        Handle the complete/mark command.
        Usage: complete id or interactive input
        """
        if not args:
            task_id_input = input("Enter task ID to mark: ").strip()
            if not task_id_input:
                print("Error: Task ID is required")
                return
            try:
                task_id = int(task_id_input)
            except ValueError:
                print("Error: Task ID must be a number")
                return
        else:
            try:
                task_id = int(args[0])
            except ValueError:
                print("Error: Task ID must be a number")
                return
        
        task = self.storage.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found")
            return
        
        success = self.storage.toggle_task_status(task_id)
        if success:
            status = "complete" if task.completed else "pending"
            print(f"Task with ID {task_id} marked as {status}")
        else:
            print(f"Error: Could not toggle status for task with ID {task_id}")
    
    def handle_command(self, command: str, args: List[str]):
        """
        Route commands to appropriate handler functions.
        """
        if command in ["add", "a"]:
            self.handle_add(args)
        elif command in ["view", "list", "l"]:
            self.handle_view(args)
        elif command in ["update", "u"]:
            self.handle_update(args)
        elif command in ["delete", "d"]:
            self.handle_delete(args)
        elif command in ["complete", "mark", "c"]:
            self.handle_complete(args)
        elif command == "help":
            self.display_help()
        elif command in ["quit", "exit", "q"]:
            self.running = False
            print("Goodbye!")
        else:
            print(f"Unknown command: {command}")
            self.display_help()
    
    def run(self):
        """
        Main loop for the CLI application.
        """
        print("Welcome to the Todo Console App!")
        self.display_help()
        
        while self.running:
            try:
                user_input = input("Enter command: ").strip()
                command, args = self.parse_command(user_input)
                self.handle_command(command, args)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.running = False
            except EOFError:
                print("\nGoodbye!")
                self.running = False