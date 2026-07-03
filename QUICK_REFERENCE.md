# WelvoxAgent - Quick Reference Guide

## 📋 Project Overview

**WelvoxAgent** is a Universal AI Operating System - a complete, production-ready platform for building intelligent applications with multiple AI providers, extensible skill system, and autonomous task execution.

**Vision**: "One AI. Infinite Skills."

---

## ⚡ Quick Start (5 minutes)

```bash
# 1. Clone
git clone https://github.com/welvox-ai/welvox-agent.git
cd welvox-agent

# 2. Setup
cp .env.example .env
pnpm install

# 3. Run
docker-compose up -d
pnpm dev

# 4. Open
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## 🏗️ Architecture at a Glance

```
User Input
    ↓
Orchestrator (Intent → Plan)
    ↓
Skill Router (Select Best Skill)
    ↓
Task Executor (Run Steps)
    ↓
Memory + AI (Claude/GPT/Gemini)
    ↓
Result Composer
    ↓
User Output
```

---

## 📁 Project Structure

```
packages/
├── types/       → Shared TypeScript types
├── database/    → DB models & migrations
├── auth/        → JWT & RBAC
├── utils/       → Helper functions
├── shared/      → Constants & configs
├── prompts/     → AI prompts
├── memory/      → Vector DB & context
├── skills/      → Skill system (9 built-in)
├── agents/      → Orchestrator & executor
└── ui/          → React components

apps/
├── api/         → FastAPI backend
└── web/         → Next.js frontend
```

---

## 🔑 Key Commands

### Development
```bash
pnpm dev           # Start all services
pnpm build         # Build packages
pnpm test          # Run tests
pnpm lint          # Check code quality
pnpm type-check    # TypeScript check
pnpm format        # Format code
```

### Database
```bash
docker-compose up postgres  # Start PostgreSQL
docker-compose exec api python -m alembic upgrade head  # Migrate
```

### Docker
```bash
docker-compose up -d        # Start all
docker-compose down         # Stop all
docker-compose logs api     # View logs
```

---

## 🤖 Core Concepts

### 1. **Orchestrator**
- Detects user intent
- Selects appropriate skills
- Creates execution plan
- **File**: `packages/agents/src/orchestrator.ts`

### 2. **Skills** (9 Built-in)
1. Universal Assistant
2. Coding Expert
3. Research Agent
4. Content Creator
5. File Analyzer
6. Data Analyst
7. Email Writer
8. Project Planner
9. Automation Expert

**File**: `packages/skills/src/index.ts`

### 3. **Memory System**
- Short-term (conversation)
- Long-term (persistent)
- Semantic search (vectors)
- **File**: `packages/memory/src/index.ts`

### 4. **Tool Router**
- Routes to appropriate handlers
- Executes with retry logic
- **File**: `packages/agents/src/router.ts`

### 5. **Task Executor**
- Runs plan steps
- Supports sequential & parallel
- Error recovery
- **File**: `packages/agents/src/executor.ts`

---

## 📚 Documentation Structure

| Document | Purpose |
|----------|---------|
| `GETTING_STARTED.md` | Setup & first run |
| `ARCHITECTURE.md` | System design deep-dive |
| `API_DOCUMENTATION.md` | API endpoints & examples |
| `DEPLOYMENT.md` | Production deployment |
| `CONTRIBUTING.md` | How to contribute |
| `QUICK_REFERENCE.md` | This file |

---

## 🔗 API Quick Reference

### Auth
```
POST /api/auth/signup       → Register
POST /api/auth/login        → Login
GET  /api/auth/verify       → Check token
```

### Conversations
```
GET  /api/conversations             → List
POST /api/conversations             → Create
GET  /api/conversations/{id}        → Get one
POST /api/conversations/{id}/messages → Send message
WS   /api/conversations/{id}/ws     → Real-time
```

### Skills
```
GET /api/skills                 → List all
GET /api/skills/{id}            → Get one
POST /api/skills/{id}/execute   → Run skill
```

### Projects
```
GET  /api/projects              → List
POST /api/projects              → Create
GET  /api/projects/{id}         → Get one
POST /api/projects/{id}/tasks   → Create task
```

### Memory
```
POST /api/memory        → Store
POST /api/memory/search → Search
GET  /api/memory        → List
```

---

## 🧪 Testing

```bash
# Unit tests
pnpm test

# Specific package
cd packages/agents && pnpm test

# With coverage
pnpm test --coverage

# Watch mode
pnpm test --watch
```

---

## 🚀 Deployment

### Local (Docker Compose)
```bash
docker-compose up
```

### Kubernetes
```bash
kubectl apply -f kubernetes/
```

### AWS (ECS)
```bash
aws ecs create-service --cluster welvox --service-name api ...
```

See `DEPLOYMENT.md` for complete guides.

---

## 🔐 Environment Variables

**Critical:**
```env
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgres://...
CLERK_SECRET_KEY=sk_live_...
JWT_SECRET=random_string
```

**Optional:**
```env
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIz...
OPENROUTER_API_KEY=sk-...
```

---

## 🛠️ Adding Custom Skills

### 1. Define Skill
```typescript
const mySkill: Skill = {
  id: 'skill_my_custom',
  name: 'My Skill',
  category: 'automation',
  // ... rest of config
};
```

### 2. Register
```typescript
orchestrator.registerSkill(mySkill);
```

### 3. Use
The skill automatically becomes available when relevant!

---

## 💾 Database Schema

**Key Tables:**
- `users` - User accounts
- `conversations` - Chat sessions
- `messages` - Chat messages
- `projects` - Work projects
- `tasks` - Project tasks
- `memories` - User memories
- `artifacts` - Generated files
- `skills` - Skill definitions

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` → `kill -9 <PID>` |
| DB connection fails | Check `DATABASE_URL` in `.env` |
| Module not found | `pnpm install` → `pnpm build` |
| Type errors | `pnpm type-check` then fix |
| Build fails | Clear `node_modules` → reinstall |

---

## 📊 Performance Tips

1. **Caching**: Responses cached in Redis (1 hour)
2. **Vector DB**: Qdrant for semantic search
3. **Connection Pooling**: PostgreSQL (10 pool size)
4. **Retry Logic**: Exponential backoff (3 attempts)
5. **Async Tasks**: Long operations queued

---

## 🔐 Security Checklist

- [ ] Environment variables not in git
- [ ] HTTPS enabled in production
- [ ] API rate limiting (60 req/min)
- [ ] Database backups automated
- [ ] Audit logging enabled
- [ ] JWT tokens rotated
- [ ] CORS configured
- [ ] Input validation on all endpoints

---

## 📈 Scaling

### Single Machine
```bash
docker-compose up
```

### Multiple Machines
```bash
kubernetes/  # Use K8s manifests
```

### Global Scale
```
AWS EKS / GCP GKE / Azure AKS
+ PostgreSQL (managed)
+ Redis (managed)
+ Qdrant (managed)
+ CDN (CloudFront/Akamai)
```

---

## 🎓 Learning Resources

- **TypeScript**: https://www.typescriptlang.org/docs/
- **Next.js**: https://nextjs.org/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **Kubernetes**: https://kubernetes.io/docs/

---

## 🔗 Links

- **GitHub**: https://github.com/welvox-ai/welvox-agent
- **Docs**: https://docs.welvox.ai
- **Discord**: https://discord.gg/welvox
- **Email**: hello@welvox.ai

---

## 📝 Common Workflows

### 1. Create a New Skill
1. Add to `packages/skills/src/index.ts`
2. Create prompts in `packages/prompts/src/index.ts`
3. Add types to `packages/types/src/index.ts`
4. Test with orchestrator
5. Document in `docs/`

### 2. Add API Endpoint
1. Create route in `apps/api/routes/`
2. Add types to `packages/types/src/`
3. Register in `apps/api/main.py`
4. Document in `API_DOCUMENTATION.md`
5. Test with curl/Postman

### 3. Deploy to Production
1. Push to main branch
2. CI/CD runs tests & builds
3. Docker images pushed to registry
4. Deploy with `kubectl apply` or ECS
5. Monitor with CloudWatch/DataDog

---

## 🎯 Project Goals

- ✅ Modular AI system architecture
- ✅ Multiple AI provider support
- ✅ Extensible skill system
- ✅ Production-ready code
- ✅ Comprehensive documentation
- 🎯 Autonomous agents
- 🎯 Advanced reasoning
- 🎯 Cost optimization

---

## 📞 Support

**Having issues?**
1. Check `TROUBLESHOOTING.md`
2. Search GitHub Issues
3. Ask in GitHub Discussions
4. Email: support@welvox.ai

---

## 🎉 Next Steps

1. ✅ Read `GETTING_STARTED.md`
2. 📖 Review `ARCHITECTURE.md`
3. 🛠️ Build a custom skill
4. 🚀 Deploy to production
5. 📝 Share your project!

---

**Happy building! 🚀**
