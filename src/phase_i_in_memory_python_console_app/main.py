#!/usr/bin/env python3
"""
Main entry point for the Todo Console Application.
"""

from .cli import TodoCLI


def main():
    """
    Main function to start the Todo Console Application.
    """
    app = TodoCLI("tasks.json")
    app.run()


if __name__ == "__main__":
    main()