#!/usr/bin/env python3
"""
Example usage of the Simple Memory MCP Server

This script demonstrates how to use the various tools provided by the
Simple Memory MCP server for session-based memory management.
"""

def example_workflow():
    """
    Example workflow showing typical usage patterns.

    Note: This is a conceptual example. In practice, these calls would be made
    through the MCP protocol by a client application.
    """

    print("=== Simple Memory MCP Server - Example Workflow ===\n")

    # 1. Create sessions
    print("1. Creating memory sessions:")
    print("   create_session(name='project_ideas')")
    print("   create_session(name='meeting_notes')")
    print("   create_session(name='personal_tasks')")
    print()

    # 2. List sessions
    print("2. Listing all sessions:")
    print("   list_sessions()")
    print("   → Shows all created sessions with their IDs and memory counts")
    print()

    # 3. Add memories to different sessions
    print("3. Adding memories to sessions:")
    print("   add_memory(")
    print("     session_id='<project_ideas_id>',")
    print("     content='Build a drawing tutorial app with step-by-step guides',")
    print("     tags=['app', 'tutorial', 'drawing']")
    print("   )")
    print()
    print("   add_memory(")
    print("     session_id='<project_ideas_id>',")
    print("     content='Create a markdown blog generator with themes',")
    print("     tags=['web', 'blog', 'generator']")
    print("   )")
    print()
    print("   add_memory(")
    print("     session_id='<meeting_notes_id>',")
    print("     content='Discussed Q1 objectives and team restructuring'")
    print("   )")
    print()

    # 4. Retrieve memories from a session
    print("4. Retrieving memories from a session:")
    print("   get_memories(session_id='<project_ideas_id>')")
    print("   → Returns all memories from the project_ideas session")
    print()

    # 5. Search memories
    print("5. Searching memories:")
    print("   # Search across all sessions")
    print("   search_memories(query='app')")
    print("   → Finds memories containing 'app' in any session")
    print()
    print("   # Search within a specific session")
    print("   search_memories(query='tutorial', session_id='<project_ideas_id>')")
    print("   → Finds memories containing 'tutorial' in project_ideas session")
    print()
    print("   # Search by tags")
    print("   search_memories(query='drawing', tags=['tutorial'])")
    print("   → Finds memories containing 'drawing' that are tagged with 'tutorial'")
    print()

    # 6. Remove specific memories
    print("6. Removing specific memories:")
    print("   remove_memory(memory_id='<memory_id>')")
    print("   → Removes a specific memory by its ID")
    print()

    # 7. Clear a session
    print("7. Clearing a session (keeps session, removes all memories):")
    print("   clear_session(session_id='<meeting_notes_id>')")
    print("   → Removes all memories from meeting_notes but keeps the session")
    print()

    # 8. Delete a session
    print("8. Deleting a session completely:")
    print("   delete_session(session_id='<personal_tasks_id>')")
    print("   → Removes the session and all its memories permanently")
    print()

def example_use_cases():
    """Example use cases for the Simple Memory MCP."""

    print("=== Common Use Cases ===\n")

    print("📝 Project Management:")
    print("   • Create sessions for different projects")
    print("   • Add ideas, tasks, and notes as memories")
    print("   • Tag memories by priority, type, or status")
    print("   • Search for specific requirements or ideas")
    print()

    print("🧠 Research & Learning:")
    print("   • Create sessions for different topics")
    print("   • Store key insights, quotes, and references")
    print("   • Tag by source, importance, or category")
    print("   • Quickly find related information")
    print()

    print("💼 Meeting & Discussion Tracking:")
    print("   • One session per meeting or discussion thread")
    print("   • Add action items, decisions, and follow-ups")
    print("   • Search across all meetings for specific topics")
    print("   • Clear old sessions when projects complete")
    print()

    print("📚 Knowledge Base:")
    print("   • Create topic-specific sessions")
    print("   • Store procedures, tips, and troubleshooting steps")
    print("   • Tag by difficulty, frequency, or team")
    print("   • Search for solutions and best practices")
    print()

def example_error_handling():
    """Examples of error handling scenarios."""

    print("=== Error Handling Examples ===\n")

    print("❌ Common Errors and How to Avoid Them:")
    print()

    print("1. Empty session name:")
    print("   create_session(name='')  # ❌ Error: Session name cannot be empty")
    print("   create_session(name='My Project')  # ✅ Correct")
    print()

    print("2. Invalid session ID:")
    print("   add_memory(session_id='invalid-id', content='Test')  # ❌ Error: Session does not exist")
    print("   # Always use session IDs returned from create_session or list_sessions")
    print()

    print("3. Empty memory content:")
    print("   add_memory(session_id='valid-id', content='')  # ❌ Error: Memory content cannot be empty")
    print("   add_memory(session_id='valid-id', content='Valid content')  # ✅ Correct")
    print()

    print("4. Invalid memory ID:")
    print("   remove_memory(memory_id='invalid-id')  # ❌ Error: Memory does not exist")
    print("   # Always use memory IDs returned from add_memory or get_memories")
    print()

    print("5. Empty search query:")
    print("   search_memories(query='')  # ❌ Error: Search query cannot be empty")
    print("   search_memories(query='my search term')  # ✅ Correct")
    print()

def example_best_practices():
    """Best practices for using the Simple Memory MCP."""

    print("=== Best Practices ===\n")

    print("🎯 Session Organization:")
    print("   • Use descriptive session names")
    print("   • Create separate sessions for different contexts")
    print("   • Don't mix unrelated topics in the same session")
    print("   • Consider using date-based naming for time-sensitive sessions")
    print()

    print("🏷️ Effective Tagging:")
    print("   • Use consistent tag naming conventions")
    print("   • Tag by priority: 'high', 'medium', 'low'")
    print("   • Tag by status: 'todo', 'in-progress', 'done'")
    print("   • Tag by category: 'bug', 'feature', 'documentation'")
    print()

    print("🔍 Search Strategies:")
    print("   • Use specific keywords for better results")
    print("   • Combine content search with tag filtering")
    print("   • Search within specific sessions when appropriate")
    print("   • Use partial words if full terms don't match")
    print()

    print("🧹 Maintenance:")
    print("   • Regularly review and clean up old sessions")
    print("   • Remove outdated or completed memories")
    print("   • Use clear_session for bulk cleanup")
    print("   • Delete sessions that are no longer needed")
    print()

if __name__ == "__main__":
    example_workflow()
    print("\n" + "="*60 + "\n")
    example_use_cases()
    print("\n" + "="*60 + "\n")
    example_error_handling()
    print("\n" + "="*60 + "\n")
    example_best_practices()

    print("\n🚀 Ready to start using Simple Memory MCP!")
    print("Run the server with: uvx git+https://github.com/bhubbb/mcm-simple-memory.git")
