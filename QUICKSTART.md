# WelvoxAgent - 5 Minute Quick Start

Get WelvoxAgent running locally in 5 minutes!

## Prerequisites (2 min)

- Docker & Docker Compose installed
- Node.js 18+ (for local development)
- Python 3.11+ (for API development)
- A terminal

## Setup (3 min)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/WelvoxAgent.git
cd WelvoxAgent
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local and add your API keys
nano .env.local
```

Minimum required:
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
CLERK_SECRET_KEY=your-clerk-secret
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-publishable-key
```

### 3. Start Everything with Docker

```bash
# Start all services
docker-compose up -d

# Wait ~30 seconds for services to initialize
sleep 30

# Check services are running
docker-compose ps
```

## Verify It's Working (1 min)

### Open in Browser

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# List skills
curl http://localhost:8000/api/skills

# Chat with agent
curl -X POST http://localhost:8000/api/agents/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! What can you help me with?"
  }'
```

## Start Developing

### Option 1: Docker Development (Recommended)

```bash
# Containers already running
# Frontend auto-reloads: http://localhost:3000
# API auto-reloads: http://localhost:8000

# View logs
docker-compose logs -f api
docker-compose logs -f web
```

### Option 2: Local Development

```bash
# Stop Docker containers
docker-compose down

# Install dependencies
pnpm install

# Start services locally
pnpm run dev

# In another terminal, start API
cd apps/api
uvicorn main:app --reload
```

## Common Commands

### Check Services

```bash
# Check what's running
docker-compose ps

# View logs
docker-compose logs

# View specific service logs
docker-compose logs -f api
docker-compose logs -f web
```

### Stop & Start

```bash
# Stop services
docker-compose down

# Start again
docker-compose up -d

# Restart
docker-compose restart

# Full restart (remove volumes)
docker-compose down -v
docker-compose up -d
```

### Database

```bash
# Access database
psql postgresql://welvox:welvox_dev_password@localhost:5432/welvox_ai

# Run migrations
pnpm db:migrate

# Seed data
pnpm db:seed

# Reset database
docker-compose down -v
docker-compose up -d
```

### Redis

```bash
# Connect to Redis
redis-cli -h localhost

# Check connection
redis-cli ping

# Clear cache
redis-cli FLUSHDB
```

## Next Steps

1. **Read Full Documentation**
   - [README.md](./README.md) - Overview
   - [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
   - [API.md](./API.md) - API reference
   - [SKILLS.md](./SKILLS.md) - Skill development

2. **Build Your First Skill**
   - Check [SKILLS.md](./SKILLS.md)
   - Create a new skill in `packages/skills/`
   - Test it in the UI

3. **Integrate a Tool**
   - Implement new tool integration in `packages/integrations/`
   - Add authentication
   - Test in API

4. **Deploy to Production**
   - See [DEPLOYMENT.md](./DEPLOYMENT.md)
   - Configure cloud platform
   - Set up monitoring

## Troubleshooting

### Services not starting

```bash
# Check Docker is running
docker --version

# Check logs
docker-compose logs

# Restart everything
docker-compose down
docker-compose up -d
```

### Port already in use

```bash
# Change ports in docker-compose.yml
# Or kill process using port:
lsof -i :8000  # Find process on port 8000
kill -9 <PID>
```

### Database connection error

```bash
# Wait longer for postgres to start
sleep 60

# Check postgres is running
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### Memory issues

```bash
# Check Docker resource limits
docker stats

# Increase Docker resources in Docker Desktop settings
```

## Getting Help

- **Docs**: Check [README.md](./README.md) and other docs
- **Issues**: [GitHub Issues](https://github.com/yourusername/WelvoxAgent/issues)
- **Discussion**: [GitHub Discussions](https://github.com/yourusername/WelvoxAgent/discussions)
- **Email**: support@welvoxai.com

## What You Have

✅ **Frontend** - Beautiful Next.js UI  
✅ **Backend** - FastAPI with LangGraph orchestration  
✅ **Database** - PostgreSQL with migrations  
✅ **Cache** - Redis for performance  
✅ **Vector DB** - Qdrant for semantic search  
✅ **Authentication** - Clerk integration  
✅ **API Docs** - Swagger UI  
✅ **Docker** - One-command deployment  

## What's Next?

1. Explore the UI at http://localhost:3000
2. Check API docs at http://localhost:8000/docs
3. Read the [README.md](./README.md)
4. Create your first custom skill
5. Integrate your first tool
6. Deploy to production

---

**You're all set! Happy coding! 🚀**

Questions? Check [CONTRIBUTING.md](./CONTRIBUTING.md) for help.
