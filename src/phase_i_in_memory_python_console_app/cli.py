import re
from typing import List, Tuple, Dict, Any
from .storage import TaskStorage
from .models import Task
from rich.console import Console
from rich.table import Table
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
    yes_no_dialog
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
        Show a simple input using the main app interface instead of dialog
        """
        try:
            from prompt_toolkit import prompt
            user_input = prompt(f"{prompt_text}: ")
            return user_input or ""
        except:
            return "quit"

    def show_message(self, title: str, text: str, pause=True):
        """
        Show a message using the console instead of a separate dialog
        """
        self.console.clear()
        rprint(f"[{self.styles['header']}]Todo Console App - {title}[/]")
        rprint(f"[{self.styles['header']}]{'='*50}[/]\n")
        rprint(text)
        if pause:
            input(f"\nPress Enter to return to menu...")

    def display_help(self):
        """
        Display help information with available commands in a styled format using console.
        """
        self.console.clear()
        rprint(f"[{self.styles['header']}]Todo Console App - Help[/]")
        rprint(f"[{self.styles['header']}]{'='*50}[/]\n")

        for cmd, info in self.commands.items():
            aliases = ', '.join(info['alias']) if info['alias'] else 'none'
            rprint(f"[bold]{cmd}[/] - {info['description']}")
            rprint(f"  [dim]aliases: {aliases}[/]\n")

        input(f"\nPress Enter to return to menu...")

    def handle_add(self):
        """
        Handle the add command with console interface.
        """
        self.console.clear()
        rprint(f"[{self.styles['header']}]Todo Console App - Add Task[/]")
        rprint(f"[{self.styles['header']}]{'='*50}[/]\n")

        title = input("Enter task title: ").strip()
        if not title:
            rprint(f"\n[{self.styles['error']}]Error: Title is required[/]")
            input(f"\nPress Enter to return to menu...")
            return

        description = input("Enter task description (optional): ").strip()
        description = description if description else None

        try:
            task_id = self.storage.add_task(title, description)
            rprint(f"\n[{self.styles['success']}]Task added successfully with ID: {task_id}[/]")
        except ValueError as e:
            rprint(f"\n[{self.styles['error']}]Error: {e}[/]")

        input(f"\nPress Enter to return to menu...")

    def handle_view(self):
        """
        Handle the view/list command with a styled display showing full descriptions.
        """
        self.console.clear()
        rprint(f"[{self.styles['header']}]Todo Console App - Your Tasks[/]")
        rprint(f"[{self.styles['header']}]{'='*50}[/]\n")

        tasks = self.storage.get_all_tasks()

        if not tasks:
            rprint(f"[{self.styles['info']}]No tasks found[/]")
            input(f"\nPress Enter to return to menu...")
            return

        from rich.panel import Panel
        from rich.columns import Columns

        for i, task in enumerate(tasks):
            status = "✓" if task.completed else "○"
            status_style = self.styles['completed'] if task.completed else self.styles['pending']
            title_style = 'white' if task.completed else 'cyan'

            # Create a panel for each task to better organize the information
            task_info = f"[bold]ID: {task.id}[/]\n"
            task_info += f"[{status_style}]{status}[/] {task.title}\n"
            task_info += f"[dim]{task.description or 'No description'}[/]" if task.description else f"[dim]No description[/]"

            panel = Panel(
                task_info,
                title=f"Task {task.id}",
                border_style="blue" if not task.completed else "green",
                expand=False
            )

            self.console.print(panel)
            # Add space between tasks
            if i < len(tasks) - 1:
                self.console.print()  # Empty line for spacing

        input(f"\nPress Enter to return to menu...")

    def handle_update(self):
        """
        Handle the update command with console interface.
        """
        self.console.clear()
        rprint(f"[{self.styles['header']}]Todo Console App - Update Task[/]")
        rprint(f"[{self.styles['header']}]{'='*50}[/]\n")

        # Show available tasks to update
        tasks = self.storage.get_all_tasks()
        if not tasks:
            rprint(f"[{self.styles['info']}]No tasks available[/]")
            input(f"\nPress Enter to return to menu...")
            return

        rprint("Available tasks:\n")
        for i, task in enumerate(tasks):
            status = "✓" if task.completed else "○"
            status_style = self.styles['completed'] if task.completed else self.styles['pending']
            rprint(f"[{i+1}] [{status_style}]{status}[/] {task.id}: {task.title}")

        print()  # Add a blank line
        task_id_str = input("Enter task ID to update: ").strip()
        try:
            task_id = int(task_id_str)
        except ValueError:
            rprint(f"\n[{self.styles['error']}]Error: Task ID must be a number[/]")
            input(f"\nPress Enter to return to menu...")
            return

        # Get the current task
        current_task = self.storage.get_task(task_id)
        if not current_task:
            rprint(f"\n[{self.styles['error']}]Error: Task with ID {task_id} not found[/]")
            input(f"\nPress Enter to return to menu...")
            return

        # Get new values
        new_title = input(f"Enter new title (current: '{current_task.title}'): ").strip()
        new_description = input(f"Enter new description (current: '{current_task.description or 'None'}'): ").strip()

        # Update the task
        success = self.storage.update_task(task_id,
                                          new_title if new_title else None,
                                          new_description if new_description else None)
        if success:
            rprint(f"\n[{self.styles['success']}]Task with ID {task_id} updated successfully[/]")
        else:
            rprint(f"\n[{self.styles['error']}]Could not update task with ID {task_id}[/]")

        input(f"\nPress Enter to return to menu...")

    def handle_delete(self):
        """
        Handle the delete command with console interface.
        """
        self.console.clear()
        rprint(f"[{self.styles['header']}]Todo Console App - Delete Task[/]")
        rprint(f"[{self.styles['header']}]{'='*50}[/]\n")

        # Show available tasks to delete
        tasks = self.storage.get_all_tasks()
        if not tasks:
            rprint(f"[{self.styles['info']}]No tasks available[/]")
            input(f"\nPress Enter to return to menu...")
            return

        rprint("Available tasks:\n")
        for i, task in enumerate(tasks):
            status = "✓" if task.completed else "○"
            status_style = self.styles['completed'] if task.completed else self.styles['pending']
            rprint(f"[{i+1}] [{status_style}]{status}[/] {task.id}: {task.title}")

        print()  # Add a blank line
        task_id_str = input("Enter task ID to delete: ").strip()
        try:
            task_id = int(task_id_str)
        except ValueError:
            rprint(f"\n[{self.styles['error']}]Error: Task ID must be a number[/]")
            input(f"\nPress Enter to return to menu...")
            return

        success = self.storage.delete_task(task_id)
        if success:
            rprint(f"\n[{self.styles['success']}]Task with ID {task_id} has been deleted[/]")
        else:
            rprint(f"\n[{self.styles['error']}]Task with ID {task_id} not found[/]")

        input(f"\nPress Enter to return to menu...")

    def handle_complete(self):
        """
        Handle the complete/mark command with console interface.
        """
        self.console.clear()
        rprint(f"[{self.styles['header']}]Todo Console App - Mark Task Complete[/]")
        rprint(f"[{self.styles['header']}]{'='*50}[/]\n")

        # Show available tasks to mark
        tasks = self.storage.get_all_tasks()
        if not tasks:
            rprint(f"[{self.styles['info']}]No tasks available[/]")
            input(f"\nPress Enter to return to menu...")
            return

        rprint("Available tasks:\n")
        for i, task in enumerate(tasks):
            status = "✓" if task.completed else "○"
            status_style = self.styles['completed'] if task.completed else self.styles['pending']
            rprint(f"[{i+1}] [{status_style}]{status}[/] {task.id}: {task.title}")

        print()  # Add a blank line
        task_id_str = input("Enter task ID to mark: ").strip()
        try:
            task_id = int(task_id_str)
        except ValueError:
            rprint(f"\n[{self.styles['error']}]Error: Task ID must be a number[/]")
            input(f"\nPress Enter to return to menu...")
            return

        task = self.storage.get_task(task_id)
        if not task:
            rprint(f"\n[{self.styles['error']}]Error: Task with ID {task_id} not found[/]")
            input(f"\nPress Enter to return to menu...")
            return

        success = self.storage.toggle_task_status(task_id)
        if success:
            new_status = "complete" if task.completed else "pending"
            status_style = self.styles['completed'] if task.completed else self.styles['pending']
            rprint(f"\n[{self.styles['success']}]Task with ID {task_id} marked as [{status_style}]{new_status}[/]")
        else:
            rprint(f"\n[{self.styles['error']}]Could not toggle status for task with ID {task_id}[/]")

        input(f"\nPress Enter to return to menu...")

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