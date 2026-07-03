# WelvoxAgent API Documentation

## Base URL
```
Development: http://localhost:8000
Production: https://api.welvox.ai
```

## Authentication

All endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer {token}
```

### Get Authentication Token

**Endpoint:** `POST /api/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGc...",
    "token_type": "bearer"
  }
}
```

---

## Conversation Endpoints

### List Conversations

**Endpoint:** `GET /api/conversations`

**Query Parameters:**
- `skip` (int, optional): Number of conversations to skip (default: 0)
- `limit` (int, optional): Number of conversations to return (default: 20)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "conv_123",
      "title": "Startup Planning",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T14:45:00Z"
    }
  ],
  "meta": {
    "total": 5,
    "skip": 0,
    "limit": 20
  }
}
```

### Create Conversation

**Endpoint:** `POST /api/conversations`

**Request:**
```json
{
  "title": "My New Project"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "conv_124",
    "title": "My New Project",
    "messages": [],
    "created_at": "2024-01-15T15:00:00Z"
  }
}
```

### Get Conversation

**Endpoint:** `GET /api/conversations/{conversation_id}`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "conv_123",
    "title": "Startup Planning",
    "messages": [
      {
        "id": "msg_1",
        "role": "user",
        "content": "Build me a website",
        "created_at": "2024-01-15T10:30:00Z"
      },
      {
        "id": "msg_2",
        "role": "assistant",
        "content": "I'll help you build a website...",
        "created_at": "2024-01-15T10:31:00Z"
      }
    ]
  }
}
```

### Send Message

**Endpoint:** `POST /api/conversations/{conversation_id}/messages`

**Request:**
```json
{
  "content": "Generate a landing page copy"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "userMessage": {
      "id": "msg_3",
      "role": "user",
      "content": "Generate a landing page copy",
      "created_at": "2024-01-15T15:05:00Z"
    },
    "aiResponse": {
      "id": "msg_4",
      "role": "assistant",
      "content": "Here's compelling landing page copy...",
      "metadata": {
        "model": "claude-opus-4-1",
        "tokens": {
          "input": 150,
          "output": 450
        }
      },
      "created_at": "2024-01-15T15:06:00Z"
    }
  }
}
```

### Get Messages

**Endpoint:** `GET /api/conversations/{conversation_id}/messages`

**Query Parameters:**
- `skip` (int, optional): Default 0
- `limit` (int, optional): Default 50, Max 100

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "msg_1",
      "role": "user",
      "content": "Hello",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "total": 10,
    "skip": 0,
    "limit": 50
  }
}
```

### Delete Conversation

**Endpoint:** `DELETE /api/conversations/{conversation_id}`

**Response:**
```json
{
  "success": true,
  "message": "Conversation deleted"
}
```

---

## Skills Endpoints

### List Skills

**Endpoint:** `GET /api/skills`

**Query Parameters:**
- `category` (string, optional): Filter by category
  - Values: `assistant`, `coding`, `research`, `content`, `data`, `file`, `communication`, `analytics`, `planning`, `automation`
- `skip` (int, optional): Default 0
- `limit` (int, optional): Default 20

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "skill_coding_expert",
      "name": "Coding Expert",
      "description": "Generate production-ready code",
      "category": "coding",
      "icon": "💻",
      "enabled": true,
      "version": "1.0.0"
    }
  ],
  "meta": {
    "total": 9,
    "skip": 0,
    "limit": 20
  }
}
```

### Get Skill Details

**Endpoint:** `GET /api/skills/{skill_id}`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "skill_coding_expert",
    "name": "Coding Expert",
    "description": "Generate production-ready code with full explanations",
    "category": "coding",
    "icon": "💻",
    "version": "1.0.0",
    "enabled": true,
    "metadata": {
      "author": "Welvox AI",
      "license": "MIT",
      "tags": ["code", "programming", "typescript"],
      "inputSchema": {
        "language": "string",
        "requirements": "string"
      },
      "outputSchema": {
        "code": "string",
        "explanation": "string"
      }
    },
    "prompts": [
      {
        "id": "prompt_1",
        "name": "Generate Code",
        "template": "Generate code for..."
      }
    ],
    "tools": [
      {
        "id": "code_executor",
        "name": "Code Executor",
        "description": "Execute and test code"
      }
    ]
  }
}
```

### Execute Skill

**Endpoint:** `POST /api/skills/{skill_id}/execute`

**Request:**
```json
{
  "language": "typescript",
  "requirements": "A function that calculates fibonacci"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "skillId": "skill_coding_expert",
    "skillName": "Coding Expert",
    "result": "Here's the code...",
    "status": "completed",
    "duration": 3500,
    "tokens": {
      "input": 200,
      "output": 500
    }
  }
}
```

---

## Projects Endpoints

### List Projects

**Endpoint:** `GET /api/projects`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "proj_1",
      "name": "My Startup Website",
      "description": "Building a SaaS landing page",
      "status": "active",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "meta": {
    "total": 3,
    "skip": 0,
    "limit": 20
  }
}
```

### Create Project

**Endpoint:** `POST /api/projects`

**Request:**
```json
{
  "name": "My Startup Website",
  "description": "Building a SaaS landing page"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "proj_2",
    "name": "My Startup Website",
    "description": "Building a SaaS landing page",
    "status": "planning",
    "tasks": [],
    "artifacts": [],
    "created_at": "2024-01-15T15:30:00Z"
  }
}
```

### Get Project

**Endpoint:** `GET /api/projects/{project_id}`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "proj_1",
    "name": "My Startup Website",
    "description": "Building a SaaS landing page",
    "status": "active",
    "tasks": [
      {
        "id": "task_1",
        "title": "Design homepage",
        "status": "in_progress",
        "priority": "high"
      }
    ],
    "artifacts": [
      {
        "id": "art_1",
        "type": "code",
        "title": "Homepage component",
        "content": "..."
      }
    ],
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

### Create Task

**Endpoint:** `POST /api/projects/{project_id}/tasks`

**Request:**
```json
{
  "title": "Design homepage",
  "description": "Create a modern homepage design"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task_2",
    "projectId": "proj_1",
    "title": "Design homepage",
    "description": "Create a modern homepage design",
    "status": "pending",
    "priority": "medium",
    "created_at": "2024-01-15T15:45:00Z"
  }
}
```

---

## Memory Endpoints

### Store Memory

**Endpoint:** `POST /api/memory`

**Request:**
```json
{
  "type": "long_term",
  "content": "User prefers dark mode and works in tech",
  "importance": 0.8,
  "tags": ["preference", "user_profile"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "mem_1",
    "type": "long_term",
    "content": "User prefers dark mode and works in tech",
    "importance": 0.8,
    "tags": ["preference", "user_profile"],
    "created_at": "2024-01-15T15:50:00Z"
  }
}
```

### Search Memory

**Endpoint:** `POST /api/memory/search`

**Request:**
```json
{
  "query": "user preferences",
  "limit": 5
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "mem_1",
      "content": "User prefers dark mode...",
      "similarity": 0.92,
      "importance": 0.8
    }
  ]
}
```

### List Memory

**Endpoint:** `GET /api/memory`

**Query Parameters:**
- `type` (string, optional): Filter by type
- `skip` (int, optional): Default 0
- `limit` (int, optional): Default 20

---

## WebSocket Endpoints

### Connect to Conversation

**Endpoint:** `WS /api/conversations/{conversation_id}/ws`

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/conversations/conv_123/ws');

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Message:', data);
};

ws.onerror = (error) => {
  console.error('Error:', error);
};
```

**Message Format:**
```json
{
  "type": "message",
  "message": {
    "id": "msg_5",
    "role": "assistant",
    "content": "Real-time response...",
    "created_at": "2024-01-15T16:00:00Z"
  }
}
```

**Events:**
- `message` - New message received
- `typing` - User/assistant is typing
- `agent:thinking` - Agent is processing
- `agent:tool_call` - Tool being executed
- `task:progress` - Task progress update

---

## Error Responses

### Error Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {
      "field": "additional info"
    }
  }
}
```

### Common Error Codes

**400 Bad Request**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request parameters"
  }
}
```

**401 Unauthorized**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid authentication token"
  }
}
```

**403 Forbidden**
```json
{
  "success": false,
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "You don't have permission to access this resource"
  }
}
```

**404 Not Found**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

**429 Too Many Requests**
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please try again later."
  }
}
```

**500 Server Error**
```json
{
  "success": false,
  "error": {
    "code": "SERVER_ERROR",
    "message": "An internal server error occurred"
  }
}
```

---

## Rate Limiting

**Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705342800
```

**Limits:**
- 60 requests per minute (general)
- 30 requests per minute (skills)
- 10 uploads per hour

---

## Pagination

All list endpoints support pagination:

**Query Parameters:**
- `skip` - Offset (default: 0)
- `limit` - Page size (default: 20, max: 100)

**Response:**
```json
{
  "success": true,
  "data": [...],
  "meta": {
    "total": 100,
    "skip": 0,
    "limit": 20
  }
}
```

---

## Examples

### Complete Flow Example

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password"
  }'

# Response: token

# 2. Create conversation
curl -X POST http://localhost:8000/api/conversations \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project"
  }'

# Response: conversation_id

# 3. Send message
curl -X POST http://localhost:8000/api/conversations/{conversation_id}/messages \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Build me a website"
  }'

# Response: AI response
```

---

## Support

For API issues or questions:
- **Email**: api-support@welvox.ai
- **Documentation**: https://docs.welvox.ai
- **Status Page**: https://status.welvox.ai

