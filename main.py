#!/usr/bin/env python3
"""
Simple Memory MCP Server

A Model Context Protocol server that provides session-based memory storage,
allowing users to create named sessions and add/remove memories within those sessions.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any
import re

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Tool
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple-memory-mcp")

# Initialize the MCP server
server = Server("simple-memory")

# In-memory storage
sessions = {}  # session_id -> {id, name, created_at, memory_count}
memories = {}  # memory_id -> {id, session_id, content, created_at, tags}

def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())

def get_current_time() -> str:
    """Get current timestamp as ISO format string."""
    return datetime.now().isoformat()

def session_exists(session_id: str) -> bool:
    """Check if a session exists."""
    return session_id in sessions

def get_session_memories(session_id: str) -> list:
    """Get all memories for a specific session."""
    return [memory for memory in memories.values() if memory["session_id"] == session_id]

def update_session_memory_count(session_id: str):
    """Update the memory count for a session."""
    if session_id in sessions:
        sessions[session_id]["memory_count"] = len(get_session_memories(session_id))

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        Tool(
            name="create_session",
            description="Create a new memory session with a given name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the new session"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="list_sessions",
            description="List all available memory sessions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="delete_session",
            description="Delete a session and all its memories",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "ID of the session to delete"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="add_memory",
            description="Add a memory item to a specific session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "ID of the session to add memory to"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content of the memory to store"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional tags for the memory",
                        "default": []
                    }
                },
                "required": ["session_id", "content"]
            }
        ),
        Tool(
            name="get_memories",
            description="Retrieve all memories from a specific session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "ID of the session to get memories from"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="remove_memory",
            description="Remove a specific memory by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": "ID of the memory to remove"
                    }
                },
                "required": ["memory_id"]
            }
        ),
        Tool(
            name="clear_session",
            description="Remove all memories from a session (but keep the session)",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "ID of the session to clear"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="search_memories",
            description="Search memories by content across all sessions or within a specific session",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to match against memory content"
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Optional: limit search to a specific session"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: filter by tags",
                        "default": []
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """
    Handle tool execution requests.
    """
    if name == "create_session":
        return await handle_create_session(arguments)
    elif name == "list_sessions":
        return await handle_list_sessions(arguments)
    elif name == "delete_session":
        return await handle_delete_session(arguments)
    elif name == "add_memory":
        return await handle_add_memory(arguments)
    elif name == "get_memories":
        return await handle_get_memories(arguments)
    elif name == "remove_memory":
        return await handle_remove_memory(arguments)
    elif name == "clear_session":
        return await handle_clear_session(arguments)
    elif name == "search_memories":
        return await handle_search_memories(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_create_session(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle session creation requests."""
    name = arguments.get("name")

    if not name or not name.strip():
        return [types.TextContent(
            type="text",
            text="# Session Creation Error\n\n**Error:** Session name cannot be empty"
        )]

    session_id = generate_id()
    created_at = get_current_time()

    sessions[session_id] = {
        "id": session_id,
        "name": name.strip(),
        "created_at": created_at,
        "memory_count": 0
    }

    return [
        types.TextContent(
            type="text",
            text=f"# Session Created\n\n**Session ID:** {session_id}\n**Name:** {name.strip()}\n**Created:** {created_at}\n**Memory Count:** 0"
        ),
        types.TextContent(
            type="text",
            text=f"# Session Details\n\nSuccessfully created session '{name.strip()}' with ID: `{session_id}`"
        )
    ]

async def handle_list_sessions(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle session listing requests."""
    if not sessions:
        return [types.TextContent(
            type="text",
            text="# Sessions\n\n**Total Sessions:** 0\n\nNo sessions have been created yet."
        )]

    session_list = []
    for session in sessions.values():
        session_list.append(f"- **{session['name']}** (ID: `{session['id']}`)\n  - Created: {session['created_at']}\n  - Memories: {session['memory_count']}")

    return [
        types.TextContent(
            type="text",
            text=f"# Sessions\n\n**Total Sessions:** {len(sessions)}\n\n" + "\n\n".join(session_list)
        )
    ]

async def handle_delete_session(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle session deletion requests."""
    session_id = arguments.get("session_id")

    if not session_id:
        return [types.TextContent(
            type="text",
            text="# Session Deletion Error\n\n**Error:** Session ID is required"
        )]

    if not session_exists(session_id):
        return [types.TextContent(
            type="text",
            text=f"# Session Deletion Error\n\n**Session ID:** {session_id}\n**Error:** Session does not exist"
        )]

    # Get session info before deletion
    session = sessions[session_id]
    session_memories = get_session_memories(session_id)

    # Delete all memories in the session
    memory_ids_to_delete = [memory["id"] for memory in session_memories]
    for memory_id in memory_ids_to_delete:
        del memories[memory_id]

    # Delete the session
    del sessions[session_id]

    return [types.TextContent(
        type="text",
        text=f"# Session Deleted\n\n**Session:** {session['name']}\n**Session ID:** {session_id}\n**Memories Deleted:** {len(memory_ids_to_delete)}\n**Status:** Successfully deleted"
    )]

async def handle_add_memory(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle memory addition requests."""
    session_id = arguments.get("session_id")
    content = arguments.get("content")
    tags = arguments.get("tags", [])

    if not session_id:
        return [types.TextContent(
            type="text",
            text="# Memory Addition Error\n\n**Error:** Session ID is required"
        )]

    if not content or not content.strip():
        return [types.TextContent(
            type="text",
            text="# Memory Addition Error\n\n**Error:** Memory content cannot be empty"
        )]

    if not session_exists(session_id):
        return [types.TextContent(
            type="text",
            text=f"# Memory Addition Error\n\n**Session ID:** {session_id}\n**Error:** Session does not exist"
        )]

    memory_id = generate_id()
    created_at = get_current_time()

    memories[memory_id] = {
        "id": memory_id,
        "session_id": session_id,
        "content": content.strip(),
        "created_at": created_at,
        "tags": tags if isinstance(tags, list) else []
    }

    # Update session memory count
    update_session_memory_count(session_id)

    session_name = sessions[session_id]["name"]
    tags_text = f"**Tags:** {', '.join(tags)}" if tags else "**Tags:** None"

    return [
        types.TextContent(
            type="text",
            text=f"# Memory Added\n\n**Memory ID:** {memory_id}\n**Session:** {session_name} ({session_id})\n**Created:** {created_at}\n{tags_text}\n**Memory Count:** {sessions[session_id]['memory_count']}"
        ),
        types.TextContent(
            type="text",
            text=f"# Memory Content\n\n{content.strip()}"
        )
    ]

async def handle_get_memories(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle memory retrieval requests."""
    session_id = arguments.get("session_id")

    if not session_id:
        return [types.TextContent(
            type="text",
            text="# Memory Retrieval Error\n\n**Error:** Session ID is required"
        )]

    if not session_exists(session_id):
        return [types.TextContent(
            type="text",
            text=f"# Memory Retrieval Error\n\n**Session ID:** {session_id}\n**Error:** Session does not exist"
        )]

    session_memories = get_session_memories(session_id)
    session_name = sessions[session_id]["name"]

    if not session_memories:
        return [types.TextContent(
            type="text",
            text=f"# Memories from '{session_name}'\n\n**Session ID:** {session_id}\n**Memory Count:** 0\n\nNo memories found in this session."
        )]

    # Sort memories by creation time (newest first)
    session_memories.sort(key=lambda x: x["created_at"], reverse=True)

    results = [
        types.TextContent(
            type="text",
            text=f"# Memories from '{session_name}'\n\n**Session ID:** {session_id}\n**Memory Count:** {len(session_memories)}"
        )
    ]

    for i, memory in enumerate(session_memories, 1):
        tags_text = f" | Tags: {', '.join(memory['tags'])}" if memory['tags'] else ""
        results.append(types.TextContent(
            type="text",
            text=f"# Memory {i}\n\n**ID:** {memory['id']}\n**Created:** {memory['created_at']}{tags_text}\n\n{memory['content']}"
        ))

    return results

async def handle_remove_memory(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle memory removal requests."""
    memory_id = arguments.get("memory_id")

    if not memory_id:
        return [types.TextContent(
            type="text",
            text="# Memory Removal Error\n\n**Error:** Memory ID is required"
        )]

    if memory_id not in memories:
        return [types.TextContent(
            type="text",
            text=f"# Memory Removal Error\n\n**Memory ID:** {memory_id}\n**Error:** Memory does not exist"
        )]

    memory = memories[memory_id]
    session_id = memory["session_id"]
    session_name = sessions[session_id]["name"] if session_id in sessions else "Unknown"

    # Remove the memory
    del memories[memory_id]

    # Update session memory count
    if session_id in sessions:
        update_session_memory_count(session_id)

    return [types.TextContent(
        type="text",
        text=f"# Memory Removed\n\n**Memory ID:** {memory_id}\n**Session:** {session_name} ({session_id})\n**Content:** {memory['content'][:100]}{'...' if len(memory['content']) > 100 else ''}\n**Status:** Successfully removed"
    )]

async def handle_clear_session(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle session clearing requests."""
    session_id = arguments.get("session_id")

    if not session_id:
        return [types.TextContent(
            type="text",
            text="# Session Clear Error\n\n**Error:** Session ID is required"
        )]

    if not session_exists(session_id):
        return [types.TextContent(
            type="text",
            text=f"# Session Clear Error\n\n**Session ID:** {session_id}\n**Error:** Session does not exist"
        )]

    session_memories = get_session_memories(session_id)
    memory_count = len(session_memories)
    session_name = sessions[session_id]["name"]

    # Remove all memories from this session
    memory_ids_to_delete = [memory["id"] for memory in session_memories]
    for memory_id in memory_ids_to_delete:
        del memories[memory_id]

    # Update session memory count
    update_session_memory_count(session_id)

    return [types.TextContent(
        type="text",
        text=f"# Session Cleared\n\n**Session:** {session_name}\n**Session ID:** {session_id}\n**Memories Removed:** {memory_count}\n**Status:** Session cleared but preserved"
    )]

async def handle_search_memories(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle memory search requests."""
    query = arguments.get("query")
    session_id = arguments.get("session_id")
    tags_filter = arguments.get("tags", [])

    if not query or not query.strip():
        return [types.TextContent(
            type="text",
            text="# Memory Search Error\n\n**Error:** Search query cannot be empty"
        )]

    # Determine which memories to search
    if session_id:
        if not session_exists(session_id):
            return [types.TextContent(
                type="text",
                text=f"# Memory Search Error\n\n**Session ID:** {session_id}\n**Error:** Session does not exist"
            )]
        search_memories = get_session_memories(session_id)
        search_scope = f"session '{sessions[session_id]['name']}'"
    else:
        search_memories = list(memories.values())
        search_scope = "all sessions"

    # Perform search
    query_lower = query.strip().lower()
    matching_memories = []

    for memory in search_memories:
        # Check content match
        content_match = query_lower in memory["content"].lower()

        # Check tag filter
        if tags_filter:
            tag_match = any(tag in memory["tags"] for tag in tags_filter)
        else:
            tag_match = True

        if content_match and tag_match:
            matching_memories.append(memory)

    # Sort by creation time (newest first)
    matching_memories.sort(key=lambda x: x["created_at"], reverse=True)

    # Prepare results
    tags_text = f" | Tags filter: {', '.join(tags_filter)}" if tags_filter else ""

    if not matching_memories:
        return [types.TextContent(
            type="text",
            text=f"# Search Results\n\n**Query:** {query}\n**Scope:** {search_scope}{tags_text}\n**Results:** 0\n\nNo memories found matching your search criteria."
        )]

    results = [
        types.TextContent(
            type="text",
            text=f"# Search Results\n\n**Query:** {query}\n**Scope:** {search_scope}{tags_text}\n**Results:** {len(matching_memories)}"
        )
    ]

    for i, memory in enumerate(matching_memories, 1):
        session_name = sessions.get(memory["session_id"], {}).get("name", "Unknown")
        tags_text = f" | Tags: {', '.join(memory['tags'])}" if memory['tags'] else ""

        # Highlight query matches in content (simple approach)
        highlighted_content = memory["content"]
        if query_lower in memory["content"].lower():
            # Find all occurrences and highlight them
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            highlighted_content = pattern.sub(f"**{query}**", memory["content"])

        results.append(types.TextContent(
            type="text",
            text=f"# Result {i}\n\n**Memory ID:** {memory['id']}\n**Session:** {session_name} ({memory['session_id']})\n**Created:** {memory['created_at']}{tags_text}\n\n{highlighted_content}"
        ))

    return results

async def main():
    # Run the server using stdin/stdout streams
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="simple-memory",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def cli():
    """Entry point for the mcp-simple-memory command."""
    asyncio.run(main())

if __name__ == "__main__":
    cli()
