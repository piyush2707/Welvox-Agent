<p align="center">
  <img src="logo.png" width="180">
</p>

<h1 align="center">Welvox-Agent</h1>

<p align="center">
Universal AI Operating System
<p align="center">

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11-green.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

</p>
## Universal AI Operating System

**One AI. Infinite Skills.**

WelvoxAgent is a production-ready, full-stack AI operating system that intelligently understands user requests, breaks them into subtasks, routes them to specialized AI skills, executes them autonomously, and delivers complete results.

## 🎯 Vision

Instead of choosing between 20 different AI tools, users interact with one unified, intelligent system that automatically:

- **Understands Intent** - Detects what you're trying to accomplish
- **Plans Execution** - Breaks complex tasks into manageable steps
- **Routes Intelligently** - Selects the right skills and tools
- **Executes Autonomously** - Runs tasks without constant guidance
- **Maintains Context** - Remembers across conversations via RAG + vector memory
- **Delivers Results** - Returns polished, actionable outputs

## 🏗️ Architecture

### Monorepo Structure

```
welvox-agent/
├── apps/
│   ├── web/                    # Next.js 15 frontend
│   └── api/                    # FastAPI Python backend
├── packages/
│   ├── types/                  # Shared TypeScript types
│   ├── database/               # Database layer (SQLAlchemy models)
│   ├── auth/                   # Authentication & authorization (Clerk)
│   ├── utils/                  # Helper utilities
│   ├── shared/                 # Shared constants & configs
│   ├── prompts/                # AI prompts & templates
│   ├── memory/                 # Memory management & RAG
│   ├── skills/                 # Skill registry & definitions
│   ├── agents/                 # Orchestration engine
│   └── ui/                     # React UI components
└── docker-compose.yml          # Local development setup
```

### Tech Stack

**Frontend:**
- Next.js 15
- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui Components
- Framer Motion

**Backend:**
- FastAPI (Python)
- LangGraph (orchestration)
- PostgreSQL (primary DB)
- Redis (caching)
- Qdrant (vector DB)

**AI Providers:**
- Anthropic Claude
- OpenAI
- Google Gemini
- OpenRouter

**Authentication:**
- Clerk

**Infrastructure:**
- Docker & Docker Compose
- GitHub Actions CI/CD
- Kubernetes-ready

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- pnpm (install with `npm install -g pnpm`)

### Setup (5 minutes)

1. **Clone & Setup**
   ```bash
   cd welvox-agent
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

2. **Start Infrastructure**
   ```bash
   docker-compose up -d
   ```
   This starts:
   - PostgreSQL (port 5432)
   - Redis (port 6379)
   - Qdrant Vector DB (port 6333)

3. **Install Dependencies**
   ```bash
   pnpm install
   ```

4. **Run Development Servers**
   ```bash
   # Terminal 1: Backend
   cd apps/api
   pip install -r requirements.txt
   python -m uvicorn main:app --reload

   # Terminal 2: Frontend
   cd apps/web
   pnpm dev
   ```

5. **Visit the App**
   - Web: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📚 Core Systems

### 1. Intent Detection & Planning

When a user sends a message, the **Orchestrator** detects intent and creates an execution plan:

```typescript
// Example: User says "Build my startup website"
const intent = await orchestrator.detectIntent(userInput);
// Returns:
// - intent: "website_builder"
// - suggestedSkills: ["content_creator", "coding_expert", "design_advisor"]
// - executionPlan: [...steps...]
```

### 2. Skill System

WelvoxAgent comes with **22+ built-in skills**, each with:
- Metadata & descriptions
- Custom prompts
- Required tools
- Input/output schemas
- Permissions

**Default Skills:**
- Universal Assistant
- Coding Expert
- Research Agent
- Content Creator
- File Analyzer
- Data Analyst
- Email Writer
- Project Planner
- Automation Expert
- ...and 13 more

### 3. Memory System

Three-layer memory management:

**Short-term** (24h TTL)
- Current conversation context
- Recent interactions
- Immediate working memory

**Long-term** (persistent)
- User preferences
- Project history
- Important facts
- Settings

**Semantic** (vector-based)
- Relationship-based retrieval
- Semantic search via embeddings
- RAG support

```python
# Store & retrieve memory
await memory_manager.store_memory(
    userId="user_123",
    type="long_term",
    content="User prefers Python over JavaScript",
    tags=["preference", "programming"]
)

results = await memory_manager.search_semantic(query_embedding)
```

### 4. Tool & Skill Routing

The **ToolRouter** intelligently matches requests to the best skill:

```typescript
// Request comes in
const request = {
  toolName: "code_generator",
  parameters: { language: "typescript" }
};

// Router finds best skill
const result = await toolRouter.routeToolCall(toolCall, context);
```

### 5. Task Execution

The **TaskExecutor** runs skills in sequence or parallel:

```typescript
// Execute steps sequentially
const results = await executor.executeStepsSequentially(plan.steps, context);

// Or in parallel (where dependencies allow)
const results = await executor.executeStepsParallel(plan.steps, context);

// With automatic retry & exponential backoff
const result = await executor.executeWithRetry(step, context, maxRetries=3);
```

## 🔌 API Endpoints

### Conversations
```
GET    /api/conversations              # List conversations
POST   /api/conversations              # Create conversation
GET    /api/conversations/:id          # Get conversation
POST   /api/conversations/:id/messages # Send message
GET    /api/conversations/:id/messages # Get messages
DELETE /api/conversations/:id          # Delete conversation
WS     /api/conversations/ws/:id       # WebSocket for real-time
```

### Projects
```
GET    /api/projects                   # List projects
POST   /api/projects                   # Create project
GET    /api/projects/:id               # Get project
PUT    /api/projects/:id               # Update project
DELETE /api/projects/:id               # Delete project
```

### Tasks
```
GET    /api/tasks                      # List tasks
POST   /api/tasks                      # Create task
GET    /api/tasks/:id                  # Get task
PUT    /api/tasks/:id                  # Update task
DELETE /api/tasks/:id                  # Delete task
```

### Skills
```
GET    /api/skills                     # List skills
GET    /api/skills/:id                 # Get skill
POST   /api/skills/:id/execute         # Execute skill
```

### Memory (RAG)
```
GET    /api/memory                     # List memories
POST   /api/memory                     # Store memory
GET    /api/memory/:id                 # Get memory
POST   /api/memory/search              # Semantic search
DELETE /api/memory/:id                 # Delete memory
```

### Files
```
POST   /api/files/upload               # Upload file
GET    /api/files                      # List files
GET    /api/files/:id                  # Get file info
POST   /api/files/:id/analyze          # Analyze file
DELETE /api/files/:id                  # Delete file
```

## 🔐 Security Features

- **RBAC** - Role-based access control
- **API Key Management** - Secure API key generation & rotation
- **Rate Limiting** - Per-user, per-endpoint limits
- **Input Validation** - Pydantic schemas on all inputs
- **Secrets Storage** - Environment-based, encrypted
- **Audit Logging** - All actions logged
- **CORS** - Configured for frontend domain

## 🚢 Deployment

### Docker Compose (Local Dev)
```bash
docker-compose up
```

### Docker (Production)
```bash
# Build images
docker build -f apps/api/Dockerfile -t welvox-api .
docker build -f apps/web/Dockerfile -t welvox-web .

# Run
docker run -p 8000:8000 welvox-api
docker run -p 3000:3000 welvox-web
```

### Kubernetes (Enterprise)
```bash
# Build & push images to registry
docker build -f apps/api/Dockerfile -t YOUR_REGISTRY/welvox-api:latest .
docker push YOUR_REGISTRY/welvox-api:latest

# Deploy with Helm
helm install welvox ./helm -f values.yaml
```

### GitHub Actions CI/CD
```yaml
# Automatic testing, building, and deployment on push
# See .github/workflows/deploy.yml
```

## 📖 Development Guide

### Adding a New Skill

1. Create skill definition:
```typescript
const mySkill: Skill = {
  id: 'skill_my_skill',
  name: 'My Skill',
  description: '...',
  category: 'coding',
  prompts: [...],
  tools: [...],
  permissions: [...]
};
```

2. Register it:
```typescript
orchestrator.registerSkill(mySkill);
```

3. It's automatically available!

### Adding a New AI Provider

1. Create integration in `packages/agents/`:
```python
# apps/api/providers/my_provider.py
class MyProvider:
    async def complete(self, prompt, **kwargs):
        # Call your API
        pass
```

2. Update config:
```python
PROVIDERS = {
    'my_provider': MyProvider()
}
```

### Running Tests

```bash
# All tests
pnpm test

# Specific package
cd packages/agents && pnpm test

# With coverage
pnpm test --coverage
```

### Type Checking

```bash
# Check types
pnpm type-check

# Fix automatically
pnpm format
```

## 🌍 Environment Variables

Copy `.env.example` to `.env.local` and fill in:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379

# AI Providers
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Authentication
CLERK_SECRET_KEY=...
CLERK_PUBLISHABLE_KEY=...

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# File Storage
MAX_FILE_SIZE=52428800  # 50MB
```

## 📊 Database Schema

Key tables:
- `users` - User accounts & settings
- `conversations` - Chat histories
- `messages` - Individual messages
- `projects` - User projects
- `tasks` - Project tasks
- `skills` - Skill registry
- `memories` - Short/long-term memory
- `artifacts` - Generated outputs
- `api_keys` - API key management
- `audit_logs` - Activity logging

Run migrations:
```bash
cd apps/api
alembic upgrade head
```

## 🎨 UI Components

Available in `packages/ui/`:

```typescript
import { Button, Card, Input, Modal, Spinner, Toast } from '@welvox/ui';

// Use them
<Button variant="primary" size="lg">Click me</Button>
<Card><p>Content</p></Card>
<Input placeholder="Type..." />
<Spinner size="md" />
```

## 📞 API Client

Use the included client:

```typescript
import { createApiClient } from '@welvox/shared';

const client = createApiClient({
  baseURL: 'http://localhost:8000',
  authToken: 'your-token'
});

// Endpoints are type-safe
const conversations = await client.conversations.list();
const response = await client.conversations.sendMessage(convId, 'Hello');
```

## 🧪 Testing

Example test:

```typescript
// packages/agents/tests/orchestrator.test.ts
describe('Orchestrator', () => {
  it('should detect coding intent', async () => {
    const intent = await orchestrator.detectIntent('write a function');
    expect(intent.intent).toBe('coding');
    expect(intent.suggestedSkills).toContain('skill_coding_expert');
  });
});
```

## 📚 Documentation

- **Architecture**: See `ARCHITECTURE.md`
- **API Docs**: http://localhost:8000/docs (Swagger)
- **Type Definitions**: `packages/types/src/index.ts`
- **Prompts**: `packages/prompts/src/index.ts`

## 🤝 Contributing

1. Fork the repo
2. Create feature branch
3. Make changes
4. Run tests: `pnpm test`
5. Submit PR

## 📄 License

MIT

## 🎯 Roadmap

- [ ] Voice input/output (LiveKit integration)
- [ ] Real-time collaboration
- [ ] Team management
- [ ] Custom skill marketplace
- [ ] Advanced analytics dashboard
- [ ] Mobile app
- [ ] Offline mode

## 💬 Support

- GitHub Issues: [Report bugs](https://github.com/welvoxai/welvox-agent/issues)
- Discussions: [Ask questions](https://github.com/welvoxai/welvox-agent/discussions)
- Email: support@piyushsujaljoahi@gmail.com
## 🤝 Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Piyush%20Joshi-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyush2707)
---

Built with ❤️ by Welvox AI

**One AI. Infinite Skills.** ✨
