# Application Structure Specification

## Overview
This specification defines the technical architecture and file structure for the in-memory Python console todo application.

## Project Structure
```
Phase I-In-Memory Python Console App/
├── constitution.md
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── .python-version
├── specs/
│   ├── task_management.md
│   └── application_structure.md
└── src/
    └── todo_app/
        ├── __init__.py
        ├── main.py
        ├── models.py
        ├── storage.py
        └── cli.py
```

## Component Specifications

### 1. models.py
- Define the Task data class with id, title, description, and completed attributes
- Include validation for title length (1-200 chars) and description length (max 1000 chars)
- Implement proper string representation for display purposes

### 2. storage.py
- Implement TaskStorage class with in-memory storage using list/dictionary
- Methods needed:
  - add_task(title, description) -> task_id
  - get_task(task_id) -> Task
  - get_all_tasks() -> List[Task]
  - update_task(task_id, title, description) -> bool
  - delete_task(task_id) -> bool
  - toggle_task_status(task_id) -> bool
- Include proper error handling for invalid task IDs

### 3. cli.py
- Implement CLI class that handles user input and output
- Commands to implement: add, view, update, delete, complete, help, quit
- Parse user commands from input string
- Format and display tasks in a readable table format
- Handle user interaction flow

### 4. main.py
- Entry point for the application
- Initialize CLI and start the main loop
- Handle graceful shutdown on quit

## Technical Requirements

### Python Version
- Target Python 3.13+ as per requirements
- Use type hints for all functions and methods
- Follow PEP 8 style guidelines

### Dependencies
- No external dependencies required beyond standard library
- Use dataclasses and typing modules for models
- Use standard I/O for console interaction

### Error Handling
- Implement try/catch blocks where appropriate
- Provide user-friendly error messages
- Never crash the application due to invalid inputs

## User Experience Requirements

### Input Parsing
- Support both full command names (add, delete, etc.) and short forms (a, d, etc.)
- Accept parameters in various formats:
  - `add "Buy groceries" "Get milk and bread"`
  - Interactive prompts for missing parameters

### Output Formatting
- Format task list in a tabular format with clear columns
- Use appropriate symbols for task status (✓ for complete, ○ for pending)
- Provide clear feedback for all operations

### Help System
- Implement built-in help system showing all commands
- Show usage examples for each command
- Display help on `help` command or invalid command usage