# Simple Memory MCP Server

A Model Context Protocol server that provides session-based memory storage, allowing you to create named sessions and add/remove memories within those sessions.

## Features

- **Session Management**: Create, list, and delete named memory sessions
- **Memory Operations**: Add, retrieve, remove, and search memories within sessions
- **In-Memory Storage**: Fast, lightweight storage using Python dictionaries
- **Session Isolation**: Memories are isolated between sessions
- **Search Capabilities**: Search memories by content across all sessions or within specific sessions
- **Tag Support**: Optional tagging system for better memory organization

## Installation & Setup

### Prerequisites
- Python 3.12 or higher
- `uv` package manager

### Quick Start

**Run directly with uvx:**
```bash
uvx git+https://github.com/bhubbb/mcm-simple-memory.git
```

**Or install locally:**
```bash
git clone <repository-url>
cd mcp-simple-memory
uv sync
```

## Usage

### Basic Workflow

1. **Create a session**:
   ```
   create_session(name="project_ideas")
   ```

2. **Add memories**:
   ```
   add_memory(session_id="<session-id>", content="Build a drawing tutorial app")
   add_memory(session_id="<session-id>", content="Create a markdown blog generator", tags=["web", "blog"])
   ```

3. **Retrieve memories**:
   ```
   get_memories(session_id="<session-id>")
   ```

4. **Search memories**:
   ```
   search_memories(query="drawing")
   search_memories(query="app", session_id="<session-id>")
   ```

## Available Tools

### Session Management

- **`create_session`** - Create a new memory session
  - `name` (required): Name for the session

- **`list_sessions`** - List all available sessions
  - No parameters

- **`delete_session`** - Delete a session and all its memories
  - `session_id` (required): ID of the session to delete

### Memory Operations

- **`add_memory`** - Add a memory to a session
  - `session_id` (required): Target session ID
  - `content` (required): Memory content
  - `tags` (optional): Array of tags

- **`get_memories`** - Retrieve all memories from a session
  - `session_id` (required): Session ID to retrieve from

- **`remove_memory`** - Remove a specific memory
  - `memory_id` (required): ID of the memory to remove

- **`clear_session`** - Remove all memories from a session (keeps session)
  - `session_id` (required): Session ID to clear

- **`search_memories`** - Search memories by content
  - `query` (required): Search query
  - `session_id` (optional): Limit search to specific session
  - `tags` (optional): Filter by tags

## Integration with AI Assistants

This MCP server is designed to work with AI assistants that support the Model Context Protocol. Configure your AI assistant to connect to this server via stdio.

Example configuration for Claude Desktop:
```json
{
  "mcpServers": {
    "simple-memory": {
      "command": "uvx",
      "args": ["git+https://github.com/bhubbb/mcm-simple-memory.git"]
    }
  }
}
```

Or if using a local installation:
```json
{
  "mcpServers": {
    "simple-memory": {
      "command": "uv",
      "args": ["run", "python", "/path/to/mcp-simple-memory/main.py"]
    }
  }
}
```

## Development

This project follows the KISS principle and uses:
- **uv** for dependency management and running
- **Single file implementation** (`main.py`)
- **In-memory storage** for simplicity
- **Standard library** features where possible

### Running

**Run directly with uvx:**
```bash
uvx git+https://github.com/bhubbb/mcm-simple-memory.git
```

**Or with local installation:**
```bash
cd mcp-simple-memory
uv run python main.py
```

### Project Structure

```
mcp-simple-memory/
├── AGENT.md          # Project rules and guidelines
├── main.py           # Single-file MCP server implementation
├── pyproject.toml    # Project configuration
├── README.md         # This file
└── .python-version   # Python version specification
```

## Data Model

### Session
```json
{
  "id": "uuid",
  "name": "string",
  "created_at": "ISO datetime",
  "memory_count": "integer"
}
```

### Memory
```json
{
  "id": "uuid",
  "session_id": "uuid",
  "content": "string",
  "created_at": "ISO datetime",
  "tags": ["string", "..."]
}
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Keep it simple (KISS principle)
2. Use `uv` for everything
3. Maintain single-file implementation
4. Follow existing code patterns
5. Ensure session isolation
6. Handle errors gracefully