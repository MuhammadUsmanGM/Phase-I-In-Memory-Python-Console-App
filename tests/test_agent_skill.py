#!/usr/bin/env python3
"""
Test script to verify the agent skill functionality for reusable intelligence.
"""

import sys
import os
# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from phase_i_in_memory_python_console_app.agent_skill import TodoAgentSkill


def test_agent_skill():
    """Test the TodoAgentSkill functionality"""
    print("Testing TodoAgentSkill...")
    
    skill = TodoAgentSkill()
    
    # Test adding a task
    result = skill.add_task("Test task", "Test description")
    assert result["success"] == True
    task_id = result["task_id"]
    print("PASS: Agent skill - Add task works")
    
    # Verify the task was added
    result = skill.get_task(task_id)
    assert result["success"] == True
    task = result["task"]
    assert task["title"] == "Test task"
    assert task["description"] == "Test description"
    assert task["completed"] == False
    print("PASS: Agent skill - Get task works")
    
    # Test viewing tasks
    result = skill.view_tasks()
    assert result["success"] == True
    tasks = result["tasks"]
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    print("PASS: Agent skill - View tasks works")
    
    # Test updating a task
    result = skill.update_task(task_id, "Updated task", "Updated description")
    assert result["success"] == True
    print("PASS: Agent skill - Update task works")
    
    # Verify the update
    result = skill.get_task(task_id)
    assert result["success"] == True
    task = result["task"]
    assert task["title"] == "Updated task"
    assert task["description"] == "Updated description"
    print("PASS: Agent skill - Update verification works")
    
    # Test marking task as complete
    result = skill.mark_task_complete(task_id)
    assert result["success"] == True
    print("PASS: Agent skill - Mark task complete works")
    
    # Verify the completion status changed
    result = skill.get_task(task_id)
    assert result["success"] == True
    task = result["task"]
    assert task["completed"] == True
    print("PASS: Agent skill - Mark complete verification works")
    
    # Test marking back as incomplete
    result = skill.mark_task_complete(task_id)
    assert result["success"] == True
    
    # Test deleting a task
    result = skill.delete_task(task_id)
    assert result["success"] == True
    print("PASS: Agent skill - Delete task works")
    
    # Verify the task was deleted
    result = skill.get_task(task_id)
    assert result["success"] == False
    print("PASS: Agent skill - Delete verification works")
    
    # Test error handling - non-existent task
    result = skill.get_task(999)
    assert result["success"] == False
    assert "not found" in result["error"]
    print("PASS: Agent skill - Error handling works")
    
    print("All agent skill tests passed!\n")


def test_agent_skill_validation():
    """Test the agent skill validation functionality"""
    print("Testing agent skill validation...")
    
    skill = TodoAgentSkill()
    
    # Test title validation (too short)
    result = skill.add_task("", "Description")
    assert result["success"] == False
    print("PASS: Agent skill - Title validation (min length) works")
    
    # Test title validation (too long)
    long_title = "x" * 201
    result = skill.add_task(long_title, "Description")
    assert result["success"] == False
    print("PASS: Agent skill - Title validation (max length) works")
    
    # Test description validation (too long)
    long_desc = "x" * 1001
    result = skill.add_task("Valid title", long_desc)
    assert result["success"] == False
    print("PASS: Agent skill - Description validation works")
    
    print("All validation tests passed!\n")


def main():
    """Run all agent skill tests"""
    print("Running Todo Agent Skill tests...\n")
    
    test_agent_skill()
    test_agent_skill_validation()
    
    print("All agent skill tests passed! Reusable intelligence is working correctly.")


if __name__ == "__main__":
    main()