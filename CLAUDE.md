# Todo Console App - Claude Code Instructions

## Project Overview
This is Phase I of the Todo Evolution project: an In-Memory Python Console App. The goal is to create a command-line todo application that stores tasks in memory, implementing all 5 Basic Level features using spec-driven development.

## Project Structure
- constitution.md - Project overview and constraints
- specs/ - Specification files for all features
  - task_management.md - Specifications for all 5 Basic Level features
  - application_structure.md - Technical architecture specification
- .claude/ - Claude Code configuration and reusable intelligence
  - config.md - Reusable intelligence configuration
  - commands/
    - todo_management.skill - Todo management agent skill
- src/ - Python source code
- README.md - Setup instructions
- CLAUDE.md - This file, instructions for Claude Code

## How to Use Specifications
1. Always reference relevant specs when implementing features
2. Read @specs/task_management.md for all functional requirements
3. Read @specs/application_structure.md for technical implementation details
4. Update specs if requirements change during implementation

## Reusable Intelligence
This project includes reusable intelligence components for enhanced AI interaction:

### Agent Skills
- @.claude/commands/todo_management.skill - Provides task management capabilities for AI agents
- Functions available: add_task, view_tasks, update_task, delete_task, mark_task_complete, get_task

### Implementation
- agent_skill.py provides programmatic access to todo operations
- AI agents can use these functions to manage tasks programmatically
- Follows same business rules as console interface

## Implementation Guidelines

### Code Quality
- Follow Python PEP 8 style guidelines
- Use type hints for all functions and methods
- Write clean, readable code with appropriate comments
- Implement proper error handling

### File Structure
- Place all source code in the src/ folder
- Create a package structure: src/phase_i_in_memory_python_console_app/
- Entry point should be src/phase_i_in_memory_python_console_app/main.py

### Component Implementation
1. Create data models in src/phase_i_in_memory_python_console_app/models.py
2. Implement storage logic in src/phase_i_in_memory_python_console_app/storage.py
3. Implement CLI interface in src/phase_i_in_memory_python_console_app/cli.py
4. Create main application entry point in src/phase_i_in_memory_python_console_app/main.py
5. Implement agent skill in src/phase_i_in_memory_python_console_app/agent_skill.py

### Task Management Features to Implement
1. Add Task – Create new todo items
2. Delete Task – Remove tasks from the list
3. Update Task – Modify existing task details
4. View Task List – Display all tasks
5. Mark as Complete – Toggle task completion status

## Commands to Follow
- When implementing, reference specs: @specs/task_management.md
- For architecture, reference: @specs/application_structure.md
- For reusable intelligence, reference: @.claude/commands/todo_management.skill
- Generate all code using these specifications as input
- Do not manually write code - only use spec-driven approach

## Dependency Management
- Use UV for package management
- Keep dependencies minimal (prefer standard library)
- If dependencies are needed, add them to pyproject.toml

## Testing
- Implement console application that can be run directly
- Ensure all 5 Basic Level features work correctly
- Test all commands with various inputs
- Verify agent skill functionality for reusable intelligence