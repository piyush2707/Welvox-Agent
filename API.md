# WelvoxAgent API Reference

## Base URL

```
http://localhost:8000/api
```

## Authentication

All requests require a Bearer token from Clerk:

```bash
Authorization: Bearer <clerk_access_token>
```

## Response Format

### Success Response
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Description of error",
    "details": { ... }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## Agents API

### Chat with Agent

**POST** `/agents/chat`

Send a message to the AI agent.

**Request:**
```json
{
  "message": "Build me a startup website",
  "project_id": "optional_project_id",
  "context": {
    "user_role": "founder",
    "budget": "5000"
  }
}
```

**Response:**
```json
{
  "agent_id": "default_agent",
  "message": "I'll help you build a startup website...",
  "status": "processing",
  "skills_used": ["design", "coding"],
  "tools_used": ["github", "figma"]
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid request
- `401` - Unauthorized
- `429` - Rate limited
- `500` - Server error

### Stream Chat Response

**POST** `/agents/chat/stream`

Get streaming responses from the agent.

**Query Parameters:**
- `chunk_size` - Size of each chunk (default: 1024)

**Response:** Server-Sent Events (SSE)

```
data: {"type": "thinking", "content": "..."}
data: {"type": "message", "content": "..."}
data: {"type": "done"}
```

### List Agents

**GET** `/agents`

Get all available agents.

**Response:**
```json
[
  {
    "id": "default_agent",
    "name": "Universal Agent",
    "description": "General-purpose AI agent",
    "status": "active",
    "skills": ["universal_assistant", "coding", "research"]
  }
]
```

### Get Agent Details

**GET** `/agents/{agent_id}`

Get detailed information about an agent.

**Response:**
```json
{
  "id": "default_agent",
  "name": "Universal Agent",
  "description": "...",
  "status": "active",
  "skills": [...],
  "config": { ... }
}
```

### Create Custom Agent

**POST** `/agents`

Create a new custom agent.

**Request:**
```json
{
  "name": "My Custom Agent",
  "description": "Description",
  "skills": ["skill_id_1", "skill_id_2"],
  "config": {
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

---

## Skills API

### List All Skills

**GET** `/skills`

Get all available skills.

**Query Parameters:**
- `category` - Filter by category (coding, research, etc.)
- `enabled` - Filter enabled/disabled
- `limit` - Number of results (default: 50)
- `offset` - Pagination offset (default: 0)

**Response:**
```json
[
  {
    "id": "coding_assistant",
    "name": "Coding Assistant",
    "description": "Help with code generation and debugging",
    "category": "development",
    "enabled": true,
    "input_schema": { ... },
    "output_schema": { ... },
    "permissions": ["read", "write", "execute"]
  }
]
```

### Get Skill Details

**GET** `/skills/{skill_id}`

Get detailed information about a specific skill.

**Response:**
```json
{
  "id": "coding_assistant",
  "name": "Coding Assistant",
  "description": "...",
  "category": "development",
  "enabled": true,
  "prompt_template": "You are a coding expert...",
  "input_schema": { ... },
  "output_schema": { ... },
  "required_tools": ["github", "terminal"],
  "permissions": ["read", "write", "execute"]
}
```

### Create Custom Skill

**POST** `/skills`

Create a new custom skill.

**Request:**
```json
{
  "name": "My Skill",
  "description": "Description",
  "category": "custom",
  "prompt_template": "You are a...",
  "input_schema": { ... },
  "output_schema": { ... },
  "required_tools": []
}
```

### Update Skill

**PUT** `/skills/{skill_id}`

Update skill configuration.

**Request:**
```json
{
  "enabled": false,
  "prompt_template": "Updated template"
}
```

### Auto-discover Skills

**GET** `/skills/registry/discover`

Scan for and register new available skills.

---

## Memory API

### Get Conversation History

**GET** `/memory/conversation`

Retrieve conversation history for a session.

**Query Parameters:**
- `session_id` - Session ID (required)
- `limit` - Number of messages (default: 50)
- `offset` - Pagination offset

**Response:**
```json
{
  "session_id": "session_123",
  "messages": [
    {
      "id": "msg_1",
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Store Message

**POST** `/memory/conversation`

Store a message in conversation history.

**Request:**
```json
{
  "session_id": "session_123",
  "role": "user",
  "content": "Hello, how can you help?"
}
```

### Search Memory (RAG)

**POST** `/memory/search`

Search through all memory using semantic search.

**Request:**
```json
{
  "query": "How do I build a React app?",
  "limit": 5,
  "memory_type": "conversation"
}
```

**Response:**
```json
{
  "query": "...",
  "results": [
    {
      "id": "mem_1",
      "type": "conversation",
      "content": "React is...",
      "score": 0.92,
      "metadata": { ... }
    }
  ]
}
```

### Get Semantic Memory

**GET** `/memory/semantic`

Get learned entities and relationships.

**Query Parameters:**
- `user_id` - User ID (required)
- `entity_type` - Filter by type

**Response:**
```json
{
  "entities": [
    {
      "id": "entity_1",
      "type": "programming_language",
      "name": "Python",
      "properties": { ... }
    }
  ],
  "relationships": [
    {
      "source": "entity_1",
      "target": "entity_2",
      "type": "similar_to"
    }
  ]
}
```

### Clear Memory

**POST** `/memory/clear`

Delete memory entries.

**Request:**
```json
{
  "memory_type": "conversation",
  "older_than_days": 30
}
```

---

## Tools API

### List Available Tools

**GET** `/tools`

Get all available tool integrations.

**Response:**
```json
[
  {
    "id": "github",
    "name": "GitHub",
    "description": "Code repository management",
    "category": "development",
    "configured": false,
    "auth_required": true
  }
]
```

### Configure Tool

**POST** `/tools/{tool_id}/configure`

Authenticate and configure a tool.

**Request:**
```json
{
  "credentials": {
    "token": "ghp_xxx",
    "username": "user"
  }
}
```

### Call Tool

**POST** `/tools/call`

Execute an action on a tool.

**Request:**
```json
{
  "tool_id": "github",
  "action": "create_issue",
  "parameters": {
    "repo": "user/repo",
    "title": "Bug report",
    "body": "Description"
  }
}
```

**Response:**
```json
{
  "tool_id": "github",
  "action": "create_issue",
  "result": {
    "issue_id": "123",
    "url": "https://..."
  },
  "success": true
}
```

### Test Tool Connection

**POST** `/tools/{tool_id}/test`

Test if tool is properly configured.

**Response:**
```json
{
  "tool_id": "github",
  "status": "connected",
  "message": "Connection successful"
}
```

---

## Projects API

### List Projects

**GET** `/projects`

Get user's projects.

**Query Parameters:**
- `status` - Filter by status (planning, active, completed)
- `limit` - Number of results
- `offset` - Pagination offset

**Response:**
```json
[
  {
    "id": "proj_123",
    "name": "My Startup",
    "description": "Building a SaaS",
    "status": "active",
    "created_at": "2024-01-01T00:00:00Z",
    "tags": ["startup", "saas"]
  }
]
```

### Create Project

**POST** `/projects`

Create a new project.

**Request:**
```json
{
  "name": "My Website",
  "description": "Building my personal website",
  "tags": ["web", "portfolio"]
}
```

### Get Project

**GET** `/projects/{project_id}`

Get project details.

### Update Project

**PUT** `/projects/{project_id}`

Update project information.

**Request:**
```json
{
  "name": "Updated name",
  "status": "completed"
}
```

### Delete Project

**DELETE** `/projects/{project_id}`

Delete a project.

### Get Project Tasks

**GET** `/projects/{project_id}/tasks`

Get all tasks in a project.

**Response:**
```json
[
  {
    "id": "task_1",
    "title": "Design homepage",
    "description": "Create homepage mockup",
    "status": "in_progress",
    "assigned_to": "skill_id"
  }
]
```

### Create Task

**POST** `/projects/{project_id}/tasks`

Create a task in the project.

**Request:**
```json
{
  "title": "Build API",
  "description": "Create REST API for frontend"
}
```

### Update Task

**PUT** `/projects/{project_id}/tasks/{task_id}`

Update task status or details.

**Request:**
```json
{
  "status": "done"
}
```

---

## Health & Status

### Health Check

**GET** `/health`

Simple health check.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Detailed Health

**GET** `/health/detailed`

Check all service dependencies.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "vector_db": "healthy"
  }
}
```

---

## Rate Limiting

- **Default**: 1000 requests per hour per user
- **Headers**:
  - `X-RateLimit-Limit`: Total requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Reset timestamp

Exceeding limit returns `429 Too Many Requests`.

---

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `SUCCESS` | 200 | Request successful |
| `BAD_REQUEST` | 400 | Invalid request parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid credentials |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

## Webhooks

Coming soon - subscribe to events like:
- Task completion
- Tool execution
- Memory updates
- Skill registration

---

## SDK & Client Libraries

- **Python**: `pip install welvox-agent`
- **JavaScript/Node**: `npm install welvox-agent`
- **Go**: `go get github.com/welvox/agent-go`

---

For more examples and use cases, see the documentation site.
