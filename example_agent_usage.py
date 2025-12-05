#!/usr/bin/env python3
"""
Example script demonstrating how an AI agent would use the TodoAgentSkill.
This represents the reusable intelligence component of the application.
"""

from src.phase_i_in_memory_python_console_app.agent_skill import create_skill


def example_ai_agent_usage():
    """
    Example of how an AI agent might interact with the todo management skill.
    This demonstrates the reusable intelligence concept.
    """
    print("Example: AI Agent Interacting with Todo Management Skill")
    print("=" * 55)
    
    # Create the agent skill instance
    todo_skill = create_skill()
    
    print("\n1. AI Agent: Adding a new task")
    result = todo_skill.add_task("Buy groceries", "Get milk, bread, and eggs")
    print(f"   Response: {result['message'] if result['success'] else result['error']}")
    
    print("\n2. AI Agent: Adding another task")
    result = todo_skill.add_task("Complete project report")
    print(f"   Response: {result['message'] if result['success'] else result['error']}")
    
    print("\n3. AI Agent: Viewing all tasks")
    result = todo_skill.view_tasks()
    if result['success']:
        print("   Tasks:")
        for task in result['tasks']:
            status = "[X]" if task['completed'] else "[ ]"
            print(f"     {status} {task['id']}: {task['title']}")
            if task['description']:
                print(f"         Description: {task['description']}")
    else:
        print(f"   Error: {result['error']}")
    
    print("\n4. AI Agent: Updating a task")
    result = todo_skill.update_task(1, "Buy groceries", "Get milk, bread, eggs, and cheese")
    print(f"   Response: {result['message'] if result['success'] else result['error']}")
    
    print("\n5. AI Agent: Marking a task as complete")
    result = todo_skill.mark_task_complete(1)
    print(f"   Response: {result['message'] if result['success'] else result['error']}")
    
    print("\n6. AI Agent: Viewing tasks again to see changes")
    result = todo_skill.view_tasks()
    if result['success']:
        print("   Updated tasks:")
        for task in result['tasks']:
            status = "[X]" if task['completed'] else "[ ]"
            print(f"     {status} {task['id']}: {task['title']}")
    else:
        print(f"   Error: {result['error']}")

    print("\n7. AI Agent: Getting details of a specific task")
    result = todo_skill.get_task(1)
    if result['success']:
        task = result['task']
        status = "[X]" if task['completed'] else "[ ]"
        print(f"   Task {task['id']}: {status} {task['title']}")
        print(f"   Description: {task['description']}")
        print(f"   Completed: {task['completed']}")
    else:
        print(f"   Error: {result['error']}")
    
    print("\n8. AI Agent: Deleting a completed task")
    result = todo_skill.delete_task(1)
    print(f"   Response: {result['message'] if result['success'] else result['error']}")
    
    print("\n9. AI Agent: Final task list")
    result = todo_skill.view_tasks()
    if result['success']:
        if result['tasks']:
            print("   Remaining tasks:")
            for task in result['tasks']:
                status = "[X]" if task['completed'] else "[ ]"
                print(f"     {status} {task['id']}: {task['title']}")
        else:
            print("   No tasks remaining")
    else:
        print(f"   Error: {result['error']}")
    
    print("\nThis example demonstrates how an AI agent can use the reusable intelligence")
    print("components to manage todo tasks programmatically, following the same")
    print("business rules as the console interface.")


if __name__ == "__main__":
    example_ai_agent_usage()