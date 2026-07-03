# WelvoxAgent Architecture

## System Overview

WelvoxAgent is a modular, scalable AI Operating System built on a monorepo architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (Next.js + React)                │
│        (Chat Interface, Project Manager, Skill Browser)    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/WebSocket
                           │
┌──────────────────────────▼──────────────────────────────────┐
│               API Gateway (FastAPI)                          │
│  (Auth, Routing, Rate Limiting, Validation)                │
└──────────────────────────┬──────────────────────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Orchestrator │    │ Task Executor│    │ Tool Router  │
│ (Intent Det) │    │ (Execution)  │    │ (Routing)    │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
      ┌────────────────────┼──────────────────────┐
      │                    │                      │
      ▼                    ▼                      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Skill System │    │    Memory    │    │ External AI  │
│ (9+ skills)  │    │ (Vector DB)  │    │ (Claude,etc) │
└──────────────┘    └──────────────┘    └──────────────┘
      │
      │
      ▼
┌────────────────────────────────────────────────┐
│          Data Layer (PostgreSQL, Redis)        │
└────────────────────────────────────────────────┘
```

---

## Package Architecture

### Core Packages

#### 1. **types** (`packages/types/`)
- Shared TypeScript type definitions
- Ensures type safety across entire system
- User, Conversation, Message, Skill, Memory, etc.

#### 2. **database** (`packages/database/`)
- ORM models (SQLAlchemy)
- Query builders
- Migration management
- Database initialization

#### 3. **auth** (`packages/auth/`)
- JWT token generation/verification
- Permission system (RBAC)
- API key management
- Password validation

#### 4. **utils** (`packages/utils/`)
- Helper functions
- Response builders
- String utilities
- Async utilities (retry, timeout, etc.)
- Logging

#### 5. **shared** (`packages/shared/`)
- API route constants
- WebSocket events
- Error codes
- AI models
- Feature flags

#### 6. **prompts** (`packages/prompts/`)
- System prompts for AI
- Skill-specific prompts
- Prompt templating
- Configuration for temperature, tokens, etc.

#### 7. **memory** (`packages/memory/`)
- In-memory short-term storage
- Vector similarity search
- Memory importance scoring
- Automatic cleanup

#### 8. **skills** (`packages/skills/`)
- Skill registry
- Default skills (9 built-in)
- Skill categorization
- Plugin architecture

#### 9. **agents** (`packages/agents/`)
- **Orchestrator**: Intent detection, planning
- **Executor**: Task execution, retry logic
- **Router**: Tool and skill routing
- **State Management**: Agent state handling

#### 10. **ui** (`packages/ui/`)
- Reusable React components
- Button, Card, Input, Modal, etc.
- Framer Motion animations
- Tailwind CSS styling

---

## Request Flow

### 1. User Sends Message
```
User Input
    ↓
Frontend (Chat Component)
    ↓ HTTP POST /api/conversations/{id}/messages
```

### 2. Backend Processing
```
API Gateway
    ↓ (Auth middleware)
Conversation Handler
    ↓
Store user message
    ↓
Orchestrator
    ├─ Parse intent
    ├─ Select skills
    └─ Create execution plan
    ↓
Task Executor
    ├─ Execute step 1 (Skill A)
    ├─ Execute step 2 (Skill B)
    └─ Execute step 3 (Skill C)
    ↓
Response Composer
    ├─ Gather artifacts
    ├─ Format response
    └─ Store in memory
    ↓
Send to client (WebSocket)
```

### 3. AI Response Flow
```
Message
    ↓
Determine best AI provider
    ├─ Claude (Anthropic)
    ├─ GPT-4 (OpenAI)
    ├─ Gemini (Google)
    └─ OpenRouter (Multiple)
    ↓
Load system prompt + skill prompts
    ↓
Send to LLM
    ↓
Parse LLM response
    ├─ Text content
    ├─ Tool calls
    └─ Structured output
    ↓
Execute tools if called
    ↓
Format final response
    ↓
Return to user
```

---

## Skill Execution Pipeline

### Skill Selection
```
User Intent: "Write a blog post about AI"
    ↓
Intent Parser: content_creation
    ↓
Available Skills:
- Content Creator (match: 100)
- Email Writer (match: 50)
- File Analyzer (match: 20)
    ↓
Selected: Content Creator
    ↓
Load prompts, tools, permissions
```

### Skill Execution
```
Skill: Content Creator
    ↓
Load prompt template
    ↓
Substitute variables
    ↓
Call Claude API
    ↓
Parse response
    ↓
Execute any tools
    ↓
Store artifact
    ↓
Update memory
    ↓
Return to user
```

---

## Database Schema

### Core Tables
```sql
users
├─ id (UUID)
├─ clerk_id (VARCHAR)
├─ email (VARCHAR)
├─ name (VARCHAR)
└─ settings (JSONB)

conversations
├─ id (UUID)
├─ user_id (FK)
├─ title (VARCHAR)
├─ status (VARCHAR)
└─ created_at (TIMESTAMP)

messages
├─ id (UUID)
├─ conversation_id (FK)
├─ role (VARCHAR)
├─ content (TEXT)
├─ metadata (JSONB)
└─ created_at (TIMESTAMP)

projects
├─ id (UUID)
├─ user_id (FK)
├─ name (VARCHAR)
├─ status (VARCHAR)
└─ created_at (TIMESTAMP)

tasks
├─ id (UUID)
├─ project_id (FK)
├─ title (VARCHAR)
├─ status (VARCHAR)
└─ priority (VARCHAR)

memories
├─ id (UUID)
├─ user_id (FK)
├─ type (VARCHAR)
├─ content (TEXT)
├─ embedding (VECTOR)
└─ metadata (JSONB)

artifacts
├─ id (UUID)
├─ project_id (FK)
├─ type (VARCHAR)
├─ content (TEXT)
└─ metadata (JSONB)
```

---

## Caching Strategy

### Redis Cache Layers
```
1. Session Cache
   ├─ User tokens: key_user:{userId}:session
   └─ TTL: 24 hours

2. Conversation Cache
   ├─ Recent messages: key_conv:{convId}:messages
   └─ TTL: 1 hour

3. Memory Cache
   ├─ Vectors for similarity: key_mem:vectors
   └─ TTL: 7 days

4. Skill Cache
   ├─ Skill definitions: key_skills:all
   └─ TTL: 30 days

5. Rate Limit Cache
   ├─ API calls: key_ratelimit:{userId}:{endpoint}
   └─ TTL: 1 minute
```

---

## Vector Database (Qdrant)

### Collections
```
1. user_memories
   ├─ Vectors: 1536-dim (from embeddings)
   ├─ Metadata: user_id, type, importance
   └─ Index: HNSW

2. project_context
   ├─ Vectors: 1536-dim
   ├─ Metadata: project_id, artifact_id
   └─ Index: HNSW

3. skill_embeddings
   ├─ Vectors: 1536-dim
   ├─ Metadata: skill_id, category
   └─ Index: HNSW
```

### Semantic Search
```
User Query: "Find memories about my startup idea"
    ↓
Generate embedding (Claude)
    ↓
Search Qdrant (similarity threshold: 0.7)
    ↓
Return top 5 results
    ↓
Rank by importance
    ↓
Include in context
```

---

## Error Handling

### Error Types
```
1. Validation Errors
   └─ 422: UNPROCESSABLE_ENTITY

2. Authentication Errors
   └─ 401: UNAUTHORIZED

3. Authorization Errors
   └─ 403: FORBIDDEN

4. Not Found Errors
   └─ 404: NOT_FOUND

5. Rate Limit Errors
   └─ 429: RATE_LIMITED

6. Server Errors
   └─ 500: INTERNAL_SERVER_ERROR
```

### Retry Strategy
```
Task Execution
    ↓ Failed
Check if retryable (network, temporary failure)
    ↓
Retry with exponential backoff
    ├─ Attempt 1: immediate
    ├─ Attempt 2: 2 seconds
    ├─ Attempt 3: 4 seconds
    └─ Attempt 4: 8 seconds
    ↓ Still failing
Return error to user
```

---

## Security Architecture

### Authentication Flow
```
User Login
    ↓
Clerk SSO
    ├─ Google
    ├─ GitHub
    └─ Email/Password
    ↓
Get user from DB (or create)
    ↓
Generate JWT token
    ↓
Return token + user data
    ↓
Frontend stores in secure storage
    ↓
Include in Authorization header for requests
```

### Permission Model
```
RBAC (Role-Based Access Control)
    ├─ User
    ├─ Admin
    └─ Moderator

Resource Permissions
    ├─ conversations: read, write, delete
    ├─ projects: read, write, delete
    ├─ skills: execute
    ├─ artifacts: read, write, delete
    └─ memory: read, write, delete
```

---

## Scaling Considerations

### Horizontal Scaling
```
Multiple API instances
    ↓
Load balancer (nginx, AWS ALB)
    ├─ Instance 1
    ├─ Instance 2
    └─ Instance 3
    ↓
Shared database (PostgreSQL)
    ↓
Distributed cache (Redis Cluster)
    ↓
Distributed vector DB (Qdrant Cluster)
```

### Task Queue (for long-running tasks)
```
User request
    ↓
Check if task is long-running (>5s)
    ├─ No: Execute immediately
    └─ Yes: Queue task
        ↓
        Add to Redis queue
        ↓
        Worker processes
        ↓
        Store result
        ↓
        Notify user via WebSocket
```

---

## Monitoring & Observability

### Key Metrics
```
1. API Performance
   ├─ Response times (p50, p95, p99)
   ├─ Request throughput
   ├─ Error rates
   └─ Cache hit rate

2. Skill Performance
   ├─ Execution times
   ├─ Success/failure rate
   ├─ Token usage
   └─ Cost per skill

3. System Health
   ├─ Database connections
   ├─ Memory usage
   ├─ Disk usage
   └─ CPU usage
```

### Logging
```
Structured logging (JSON)
    ├─ Request ID (trace)
    ├─ User ID
    ├─ Timestamp
    ├─ Level (INFO, WARN, ERROR)
    └─ Message + context
    ↓
Sent to centralized logging
    ├─ ELK stack
    ├─ DataDog
    └─ CloudWatch
```

---

## Future Architecture Enhancements

### Planned Improvements
1. **LangGraph Integration**: Better workflow orchestration
2. **Autonomous Agents**: Self-improving skill execution
3. **Multi-Agent Collaboration**: Agents working together
4. **Function Calling**: Native LLM function calls
5. **Streaming Responses**: Real-time result streaming
6. **Advanced Caching**: Intelligent cache invalidation
7. **A/B Testing**: Skill and prompt optimization
8. **Cost Optimization**: Intelligent provider selection

---

## Development Workflow

### Local Development
```
1. Modify code
2. Type check: pnpm type-check
3. Test: pnpm test
4. Build: pnpm build
5. Run: pnpm dev
```

### Production Deployment
```
1. Commit to main
2. Run tests: pnpm test
3. Build: pnpm build
4. Docker build
5. Deploy to Kubernetes/Container Registry
6. Run migrations
7. Monitor metrics
```

---

End of Architecture Documentation
