#!/usr/bin/env python3
"""
Test script to verify all functionality of the Todo Console App.
"""

import sys
import os
# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from phase_i_in_memory_python_console_app.models import Task
from phase_i_in_memory_python_console_app.storage import TaskStorage


def test_models():
    """Test the Task model functionality"""
    print("Testing Task model...")
    
    # Test basic task creation
    task = Task(id=1, title="Test task", description="Test description")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed == False
    print("PASS: Basic task creation works")

    # Test task completion toggle
    task.completed = True
    assert task.completed == True
    print("PASS: Task completion toggle works")

    # Test title validation (1-200 chars)
    try:
        Task(id=2, title="", description="Too short title")
        assert False, "Should have raised ValueError for empty title"
    except ValueError:
        print("PASS: Title validation (min length) works")

    long_title = "x" * 201
    try:
        Task(id=3, title=long_title, description="Too long title")
        assert False, "Should have raised ValueError for long title"
    except ValueError:
        print("PASS: Title validation (max length) works")

    # Test description validation (max 1000 chars)
    long_desc = "x" * 1001
    try:
        Task(id=4, title="Valid title", description=long_desc)
        assert False, "Should have raised ValueError for long description"
    except ValueError:
        print("PASS: Description validation works")

    print("All Task model tests passed!\n")


def test_storage():
    """Test the TaskStorage functionality"""
    print("Testing TaskStorage...")
    
    storage = TaskStorage()
    
    # Test adding a task
    task_id = storage.add_task("Test task", "Test description")
    assert task_id == 1
    print("PASS: Task addition works")

    # Test getting a task
    task = storage.get_task(task_id)
    assert task is not None
    assert task.id == task_id
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed == False
    print("PASS: Task retrieval works")

    # Test getting all tasks
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == task_id
    print("PASS: Get all tasks works")

    # Test updating a task
    success = storage.update_task(task_id, "Updated title", "Updated description")
    assert success == True

    updated_task = storage.get_task(task_id)
    assert updated_task.title == "Updated title"
    assert updated_task.description == "Updated description"
    print("PASS: Task update works")

    # Test toggling task status
    initial_status = updated_task.completed
    success = storage.toggle_task_status(task_id)
    assert success == True

    toggled_task = storage.get_task(task_id)
    assert toggled_task.completed != initial_status
    print("PASS: Task status toggle works")

    # Toggle back for further tests
    storage.toggle_task_status(task_id)

    # Test deleting a task
    success = storage.delete_task(task_id)
    assert success == True
    assert storage.get_task(task_id) is None
    print("PASS: Task deletion works")

    # Test operations on non-existent task
    assert storage.get_task(999) is None
    assert storage.update_task(999, "New title") == False
    assert storage.delete_task(999) == False
    assert storage.toggle_task_status(999) == False
    print("PASS: Non-existent task handling works")

    print("All TaskStorage tests passed!\n")


def test_cli_commands():
    """Test CLI command handling"""
    print("Testing CLI command handling...")
    
    # Create a CLI instance
    cli = TodoCLI()

    # Test that help command works (though we can't easily test the output)
    cli.running = False  # Stop the run loop for testing individual methods
    print("PASS: CLI instantiation works")

    # Parse some sample commands
    command, args = cli.parse_command("add \"Buy groceries\" \"Get milk\"")
    assert command == "add"
    assert args == ["Buy groceries", "Get milk"]
    print("PASS: Command parsing works")

    command, args = cli.parse_command("view")
    assert command == "view"
    assert args == []
    print("PASS: Simple command parsing works")

    command, args = cli.parse_command("update 1 \"New title\"")
    assert command == "update"
    assert args == ["1", "New title"]
    print("PASS: Update command parsing works")

    command, args = cli.parse_command("complete 1")
    assert command == "complete"
    assert args == ["1"]
    print("PASS: Complete command parsing works")

    print("All CLI tests passed!\n")


def main():
    """Run all tests"""
    print("Running Todo Console App tests...\n")
    
    test_models()
    test_storage()
    test_cli_commands()
    
    print("All tests passed! The Todo Console App is working correctly.")


if __name__ == "__main__":
    main()