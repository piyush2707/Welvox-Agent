# WelvoxAgent - Getting Started Guide

## 🚀 Quick Start

### Prerequisites
- **Node.js**: 18+ (for web and TypeScript packages)
- **Python**: 3.11+ (for FastAPI backend)
- **pnpm**: 9.0+ (package manager)
- **Docker**: 20.10+ (optional, for containerized deployment)
- **PostgreSQL**: 15+ (database)
- **Redis**: 7+ (caching and queues)

### Installation

#### 1. Clone and Setup
```bash
cd welvox-agent
cp .env.example .env
```

#### 2. Configure Environment Variables
Edit `.env` and update:
```
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
CLERK_SECRET_KEY=your_key
DATABASE_URL=postgresql://welvox:welvox@localhost:5432/welvox_db
```

#### 3. Install Dependencies
```bash
pnpm install
```

#### 4. Start Development Environment

**Option A: Local Development**

Terminal 1 - Database & Redis:
```bash
docker-compose up postgres redis qdrant
```

Terminal 2 - Backend API:
```bash
cd apps/api
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Terminal 3 - Frontend:
```bash
cd apps/web
pnpm dev
```

The app will be available at:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Option B: Docker Compose (All-in-one)**
```bash
docker-compose up
```

---

## 📁 Project Structure

```
welvox-agent/
├── apps/
│   ├── web/              # Next.js frontend
│   └── api/              # FastAPI backend
├── packages/
│   ├── types/            # Shared TypeScript types
│   ├── database/         # Database models & queries
│   ├── auth/             # Authentication utilities
│   ├── utils/            # Common utilities
│   ├── shared/           # Shared constants
│   ├── prompts/          # AI prompts & templates
│   ├── memory/           # Memory management
│   ├── skills/           # Skill system
│   ├── agents/           # AI orchestration
│   └── ui/               # React components
├── docker-compose.yml    # Local development stack
├── tsconfig.json         # TypeScript config
└── pnpm-workspace.yaml   # pnpm workspace
```

---

## 🔧 Development Guide

### Building Packages
```bash
pnpm build
```

### Running Tests
```bash
pnpm test
```

### Type Checking
```bash
pnpm type-check
```

### Formatting Code
```bash
pnpm format
```

### Linting
```bash
pnpm lint
```

---

## 🤖 Understanding WelvoxAgent

### Core Components

#### 1. **Orchestrator** (`packages/agents/src/orchestrator.ts`)
- Detects user intent
- Creates execution plans
- Routes to appropriate skills

#### 2. **Skill System** (`packages/skills/src/index.ts`)
- 9 default skills (Universal Assistant, Coding, Research, etc.)
- Extensible architecture
- Each skill has prompts, tools, and permissions

#### 3. **Memory Manager** (`packages/memory/src/index.ts`)
- Short-term (conversation) memory
- Long-term (persistent) memory
- Semantic search via vectors
- Auto-cleanup of expired memories

#### 4. **Tool Router** (`packages/agents/src/router.ts`)
- Routes tool calls to appropriate handlers
- Skill matching algorithm
- Execution with retry logic

#### 5. **Task Executor** (`packages/agents/src/executor.ts`)
- Executes plan steps sequentially or in parallel
- Retry logic with exponential backoff
- Error handling and recovery

### Workflow Example

When a user says: **"Build me a startup website"**

```
1. Intent Detection
   ↓ "content_creation + coding + planning"
   
2. Skill Selection
   ↓ ["Content Creator", "Coding Expert", "Project Planner"]
   
3. Execution Plan
   ↓ Step 1: Plan project → Step 2: Design → Step 3: Code → Step 4: Deploy
   
4. Task Execution
   ↓ Execute each step, pass outputs to next step
   
5. Result Composition
   ↓ Gather artifacts (code, docs, designs) → Present polished result
```

---

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/verify` - Verify token
- `POST /api/auth/logout` - Logout

### Conversations
- `GET /api/conversations` - List conversations
- `POST /api/conversations` - Create conversation
- `GET /api/conversations/{id}` - Get conversation
- `POST /api/conversations/{id}/messages` - Send message
- `WS /api/conversations/{id}/ws` - WebSocket for real-time

### Skills
- `GET /api/skills` - List skills
- `GET /api/skills/{id}` - Get skill details
- `POST /api/skills/{id}/execute` - Execute skill

### Projects
- `GET /api/projects` - List projects
- `POST /api/projects` - Create project
- `GET /api/projects/{id}` - Get project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Memory
- `GET /api/memory` - List memories
- `POST /api/memory` - Store memory
- `POST /api/memory/search` - Semantic search

---

## 🎨 Frontend Architecture

### Pages
- `/` - Dashboard
- `/chat` - Conversation interface
- `/projects` - Project management
- `/skills` - Skill browser
- `/settings` - User settings
- `/docs` - Documentation

### State Management (Zustand)
```typescript
// useStore.ts
import { create } from 'zustand';

interface AppState {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  addMessage: (message: Message) => void;
}

export const useStore = create<AppState>((set) => ({
  conversations: [],
  currentConversation: null,
  addMessage: (message) => {
    // Implementation
  },
}));
```

---

## 🚀 Deployment

### Production Build
```bash
pnpm build
```

### Docker Deployment
```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```

### Environment Setup
1. Set all required environment variables
2. Configure database backups
3. Set up monitoring and logging
4. Configure CDN for static assets
5. Enable SSL/TLS

### Kubernetes (Optional)
```bash
kubectl apply -f kubernetes/
```

---

## 📊 Monitoring & Logging

### Logs
- Backend: Logged to stdout and `/var/log/welvox-api.log`
- Frontend: Logged to browser console
- Database: PostgreSQL logs in container

### Metrics
- API response times
- Skill execution performance
- Memory usage
- Task success/failure rates

### Health Checks
```bash
curl http://localhost:8000/health
```

---

## 🔐 Security

### API Authentication
- JWT tokens issued on login
- Tokens expire after 24 hours
- Refresh endpoint available
- CORS configured for allowed origins

### Data Protection
- Passwords hashed with bcrypt
- API keys encrypted in database
- Environment variables for secrets
- Rate limiting on endpoints

### Audit Logging
- All user actions logged
- Database changes tracked
- Failed login attempts recorded
- Integration events logged

---

## 🧪 Testing

### Unit Tests
```bash
cd packages/agents
pnpm test
```

### Integration Tests
```bash
cd apps/api
pytest tests/
```

### E2E Tests
```bash
cd apps/web
pnpm test:e2e
```

---

## 📚 Adding Custom Skills

### 1. Create Skill Definition
```typescript
const mySkill: Skill = {
  id: 'skill_my_custom',
  name: 'My Custom Skill',
  description: 'Does something amazing',
  category: 'automation',
  icon: '⚡',
  version: '1.0.0',
  enabled: true,
  metadata: {
    author: 'Your Name',
    license: 'MIT',
    tags: ['custom', 'awesome'],
    inputSchema: { param1: 'string' },
    outputSchema: { result: 'string' },
    requiredTools: [],
  },
  prompts: [...],
  tools: [...],
  permissions: [...],
};
```

### 2. Register Skill
```typescript
import { orchestrator } from '@welvox/agents';

orchestrator.registerSkill(mySkill);
```

### 3. Use in Conversation
The skill will automatically be available when relevant to user intent!

---

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
```

**Database connection failed:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Verify connection string in .env
```

**Module not found:**
```bash
# Rebuild packages
pnpm build

# Check tsconfig paths are correct
```

---

## 📞 Support & Resources

- **Documentation**: See `/docs` directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@welvox.ai

---

## 📄 License

MIT License - See LICENSE file

---

## 🚀 Next Steps

1. ✅ Set up local development
2. 📖 Read architecture documentation
3. 🛠️ Build a custom skill
4. 🚀 Deploy to production
5. 🎉 Build amazing AI-powered features!

Happy building! 🎊
