import re
from typing import List, Tuple, Dict, Any
from .storage import TaskStorage
from .models import Task
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    HSplit,
    Window,
    HorizontalAlign,
    VerticalAlign,
    FloatContainer,
    Float,
    VSplit
)
from prompt_toolkit.layout.controls import (
    FormattedTextControl
)
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame, Box, Label
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import (
    radiolist_dialog,
    yes_no_dialog,
    input_dialog,
    message_dialog
)


class TodoCLI:
    """
    Command Line Interface for the Todo application.
    Handles user input, command parsing, and output formatting with rich styling and true key navigation.
    """

    def __init__(self):
        self.storage = TaskStorage()
        self.running = True
        self.console = Console()
        self.setup_styling()
        self.commands = {
            'add': {'alias': ['a'], 'description': 'Add a new task'},
            'view': {'alias': ['list', 'l'], 'description': 'View all tasks'},
            'update': {'alias': ['u'], 'description': 'Update a task'},
            'delete': {'alias': ['d'], 'description': 'Delete a task'},
            'complete': {'alias': ['mark', 'c'], 'description': 'Mark task as complete/incomplete'},
            'help': {'alias': [], 'description': 'Show this help'},
            'quit': {'alias': ['exit', 'q'], 'description': 'Exit application'}
        }
        self.menu_options = [
            ("add", "1. Add Task"),
            ("view", "2. View Tasks"),
            ("update", "3. Update Task"),
            ("delete", "4. Delete Task"),
            ("complete", "5. Mark Task Complete"),
            ("help", "6. Help"),
            ("quit", "7. Quit")
        ]
        self.current_menu_index = 0

    def setup_styling(self):
        """Setup color themes and styling options."""
        self.styles = {
            'header': 'bold blue',
            'success': 'bold green',
            'error': 'bold red',
            'warning': 'bold yellow',
            'info': 'cyan',
            'completed': 'green',
            'pending': 'yellow',
            'title': 'bold white',
            'description': 'dim'
        }

    def show_menu_with_navigation(self):
        """
        Show menu with actual arrow key navigation.
        """
        def get_text():
            result = []
            # BLOCK ASCII art header specifically for "TODO CONSOLE APP" using block characters
            ascii_art = [
                "  ████████╗ ██████╗ ██████╗  ██████╗ ",
                "  ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗",
                "     ██║   ██║   ██║██║  ██║██║   ██║",
                "     ██║   ██║   ██║██║  ██║██║   ██║",
                "     ██║   ╚██████╔╝██████╔╝╚██████╔╝",
                "     ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ",
                "                                      ",
                "   ██████╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██╗     ███████╗",
                "  ██╔════╝██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██║     ██╔════╝",
                "  ██║     ██║   ██║██╔██╗ ██║███████╗██║   ██║██║     █████╗  ",
                "  ██║     ██║   ██║██║╚██╗██║╚════██║██║   ██║██║     ██╔══╝  ",
                "  ╚██████╗╚██████╔╝██║ ╚████║███████║╚██████╔╝███████╗███████╗",
                "   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝",
                "                                                              ",
                "   █████╗ ██████╗ ██████╗ ",
                "  ██╔══██╗██╔══██╗██╔══██╗",
                "  ███████║██████╔╝██████╔╝",
                "  ██╔══██║██╔═══╝ ██╔═══╝ ",
                "  ██║  ██║██║     ██║     ",
                "  ╚═╝  ╚═╝╚═╝     ╚═╝     "
            ]

            for line in ascii_art:
                result.append(('class:ascii_header', line))
                result.append(('', '\n'))

            # Welcome message
            result.append(('class:welcome', "Welcome to the Enhanced Todo Console App!"))
            result.append(('', '\n\n'))
            # Navigation tip
            result.append(('class:tip', "💡 Tip: Use UP/DOWN arrow keys to navigate, ENTER to select"))
            result.append(('', '\n\n'))

            # Menu options formatted to the side
            result.append(('class:menu-title', 'Select an option:\n\n'))

            for i, (cmd, text) in enumerate(self.menu_options):
                if i == self.current_menu_index:
                    result.append(('class:menu_arrow', '> '))
                    result.append(('class:selected', f'{text}'))
                else:
                    result.append(('class:menu_space', '  '))
                    result.append(('class:unselected', f'{text}'))
                result.append(('', '\n'))

            result.append(('', '\n'))
            result.append(('class:info', 'Or type command directly (e.g., \'add\', \'view\', \'quit\')'))
            return result

        # Style for the app
        app_style = Style([
            ('header', 'bold blue'),
            ('ascii_header', 'bold yellow'),
            ('welcome', 'bold green'),
            ('tip', 'italic cyan'),
            ('menu-title', 'bold'),
            ('menu_arrow', 'bold red'),
            ('menu_space', ''),
            ('selected', 'bold reverse'),
            ('unselected', 'fg:gray'),
            ('info', 'cyan'),
            ('success', 'bold green'),
            ('error', 'bold red'),
        ])

        # Create key bindings
        bindings = KeyBindings()

        @bindings.add('up')
        def _(event):
            self.current_menu_index = max(0, self.current_menu_index - 1)

        @bindings.add('down')
        def _(event):
            self.current_menu_index = min(len(self.menu_options) - 1, self.current_menu_index + 1)

        @bindings.add('enter')
        def _(event):
            event.app.exit(result=self.menu_options[self.current_menu_index][0])

        @bindings.add('c-c')
        def _(event):
            event.app.exit(result='quit')

        # Create the application
        text_control = FormattedTextControl(get_text)
        root_container = Box(Window(text_control,
                                    always_hide_cursor=False,
                                    wrap_lines=True))

        app = Application(
            layout=Layout(root_container),
            key_bindings=bindings,
            style=app_style,
            full_screen=False
        )

        try:
            result = app.run()
            return result
        except:
            return 'quit'  # Default to quit if there's an issue

    def show_simple_input(self, prompt_text: str):
        """
        Show a simple input dialog using prompt_toolkit
        """
        try:
            result = input_dialog(
                title="Todo App",
                text=prompt_text,
                style=Style([('frame.label', 'bg:#ffffff #000000')])
            ).run()
            return result or ""
        except:
            return "quit"

    def show_message(self, title: str, text: str):
        """
        Show a message dialog
        """
        try:
            message_dialog(
                title=title,
                text=text
            ).run()
        except:
            pass

    def display_help(self):
        """
        Display help information with available commands in a styled format using dialog.
        """
        help_text = "Available Commands:\n\n"
        for cmd, info in self.commands.items():
            aliases = ', '.join(info['alias']) if info['alias'] else 'none'
            help_text += f"{cmd} - {info['description']}\n"
            help_text += f"  aliases: {aliases}\n\n"

        help_text += "Press Enter to return to main menu"
        self.show_message("Todo Console App Help", help_text)

    def handle_add(self):
        """
        Handle the add command with dialog interface.
        """
        title = self.show_simple_input("Enter task title:")
        if not title:
            self.show_message("Error", "Title is required")
            return

        description = self.show_simple_input("Enter task description (optional):")

        try:
            task_id = self.storage.add_task(title, description if description else None)
            self.show_message("Success", f"Task added successfully with ID: {task_id}")
        except ValueError as e:
            self.show_message("Error", f"Error: {e}")

    def handle_view(self):
        """
        Handle the view/list command with a styled table.
        """
        tasks = self.storage.get_all_tasks()

        if not tasks:
            self.show_message("Info", "No tasks found")
            return

        # Create a formatted text for tasks - show more of description
        tasks_text = "ID  | Status | Title                    | Description\n"
        tasks_text += "----|--------|------------------------|-----------------------------\n"

        for task in tasks:
            status = "✓" if task.completed else "○"
            title = task.title[:20] + ".." if len(task.title) > 20 else task.title
            description = task.description or ""
            # Show more of description (up to 60 chars) to reduce truncation
            if len(description) > 60:
                description = description[:57] + "..."
            tasks_text += f"{task.id:<3} | {status:^6} | {title:<22} | {description}\n"

        # Show tasks in a scrollable dialog that allows full viewing
        self.show_message("Your Tasks", tasks_text)

    def handle_update(self):
        """
        Handle the update command with dialog interface.
        """
        # Show available tasks to update
        tasks = self.storage.get_all_tasks()
        if not tasks:
            self.show_message("Info", "No tasks available")
            return

        task_list = [(str(task.id), f"{task.id}: {task.title}") for task in tasks]
        if not task_list:
            self.show_message("Info", "No tasks available")
            return

        # For simplicity, let's use a simple input to select task ID
        task_id_str = self.show_simple_input("Enter task ID to update:")
        try:
            task_id = int(task_id_str)
        except ValueError:
            self.show_message("Error", "Task ID must be a number")
            return

        # Get the current task
        current_task = self.storage.get_task(task_id)
        if not current_task:
            self.show_message("Error", f"Task with ID {task_id} not found")
            return

        # Get new values
        new_title = self.show_simple_input(f"Enter new title (current: {current_task.title}):")
        new_description = self.show_simple_input(f"Enter new description (current: {current_task.description or 'None'}):")

        # Use current values if user didn't provide new ones
        if new_title == "":
            new_title = current_task.title
        if new_description == "":
            new_description = current_task.description

        # Update the task
        success = self.storage.update_task(task_id, new_title, new_description if new_description != current_task.description else None)
        if success:
            self.show_message("Success", f"Task with ID {task_id} updated successfully")
        else:
            self.show_message("Error", f"Could not update task with ID {task_id}")

    def handle_delete(self):
        """
        Handle the delete command with dialog interface.
        """
        # Show available tasks to delete
        tasks = self.storage.get_all_tasks()
        if not tasks:
            self.show_message("Info", "No tasks available")
            return

        task_list = [(str(task.id), f"{task.id}: {task.title}") for task in tasks]
        if not task_list:
            self.show_message("Info", "No tasks available")
            return

        # Get task ID to delete
        task_id_str = self.show_simple_input("Enter task ID to delete:")
        try:
            task_id = int(task_id_str)
        except ValueError:
            self.show_message("Error", "Task ID must be a number")
            return

        success = self.storage.delete_task(task_id)
        if success:
            self.show_message("Success", f"Task with ID {task_id} has been deleted")
        else:
            self.show_message("Error", f"Task with ID {task_id} not found")

    def handle_complete(self):
        """
        Handle the complete/mark command with dialog interface.
        """
        # Show available tasks to mark
        tasks = self.storage.get_all_tasks()
        if not tasks:
            self.show_message("Info", "No tasks available")
            return

        task_list = [(str(task.id), f"{task.id}: {task.title}") for task in tasks]
        if not task_list:
            self.show_message("Info", "No tasks available")
            return

        # Get task ID to toggle
        task_id_str = self.show_simple_input("Enter task ID to mark:")
        try:
            task_id = int(task_id_str)
        except ValueError:
            self.show_message("Error", "Task ID must be a number")
            return

        task = self.storage.get_task(task_id)
        if not task:
            self.show_message("Error", f"Task with ID {task_id} not found")
            return

        success = self.storage.toggle_task_status(task_id)
        if success:
            status = "complete" if task.completed else "pending"
            self.show_message("Success", f"Task with ID {task_id} marked as {status}")
        else:
            self.show_message("Error", f"Could not toggle status for task with ID {task_id}")

    def run(self):
        """
        Main loop for the CLI application with true arrow key navigation.
        """
        while self.running:
            try:
                # Show menu with arrow key navigation
                choice = self.show_menu_with_navigation()

                if choice == 'add':
                    self.handle_add()
                elif choice == 'view':
                    self.handle_view()
                elif choice == 'update':
                    self.handle_update()
                elif choice == 'delete':
                    self.handle_delete()
                elif choice == 'complete':
                    self.handle_complete()
                elif choice == 'help':
                    self.display_help()
                elif choice == 'quit':
                    self.running = False
                    rprint(f"[{self.styles['success']}]Goodbye![/]")
                else:
                    # If user enters an invalid choice
                    continue
            except KeyboardInterrupt:
                rprint(f"\n[{self.styles['success']}]Goodbye![/]")
                self.running = False