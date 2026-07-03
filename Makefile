.PHONY: help install dev build test lint format clean docker docker-up docker-down db-migrate db-seed

help:
	@echo "WelvoxAgent Development Commands"
	@echo "================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Start development servers"
	@echo "  make dev-api          Start API dev server only"
	@echo "  make dev-web          Start web dev server only"
	@echo ""
	@echo "Building:"
	@echo "  make build            Build all packages"
	@echo "  make build-api        Build API only"
	@echo "  make build-web        Build web only"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-watch       Run tests in watch mode"
	@echo "  make test-coverage    Run tests with coverage"
	@echo ""
	@echo "Linting:"
	@echo "  make lint             Lint all code"
	@echo "  make type-check       Type check all code"
	@echo "  make format           Format all code"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate       Run database migrations"
	@echo "  make db-seed          Seed database with sample data"
	@echo "  make db-reset         Reset database (caution!)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     Build Docker images"
	@echo "  make docker-up        Start Docker containers"
	@echo "  make docker-down      Stop Docker containers"
	@echo "  make docker-logs      View container logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Clean all build artifacts"
	@echo "  make clean-node       Clean node_modules"
	@echo ""

install:
	@echo "Installing dependencies..."
	pnpm install
	cd apps/api && pip install -r requirements.txt

dev:
	@echo "Starting development servers..."
	pnpm run dev

dev-api:
	@echo "Starting API development server..."
	cd apps/api && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

dev-web:
	@echo "Starting web development server..."
	cd apps/web && npm run dev

build:
	@echo "Building all packages..."
	pnpm run build

build-api:
	@echo "Building API..."
	cd apps/api && python -m pip install -e .

build-web:
	@echo "Building web..."
	cd apps/web && npm run build

test:
	@echo "Running tests..."
	pnpm run test

test-watch:
	@echo "Running tests in watch mode..."
	pnpm run test:watch

test-coverage:
	@echo "Running tests with coverage..."
	pnpm run test -- --coverage

lint:
	@echo "Linting code..."
	pnpm run lint

type-check:
	@echo "Type checking..."
	pnpm run type-check

format:
	@echo "Formatting code..."
	pnpm run format

db-migrate:
	@echo "Running database migrations..."
	cd apps/api && alembic upgrade head

db-seed:
	@echo "Seeding database..."
	cd apps/api && python -m scripts.seed_db

db-reset:
	@echo "WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd apps/api && alembic downgrade base && alembic upgrade head; \
	fi

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Services starting... wait a moment for them to be ready"
	@echo "Frontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Qdrant: http://localhost:6333"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f

clean:
	@echo "Cleaning build artifacts..."
	rm -rf dist/ build/ .egg-info/ .next/ out/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-node:
	@echo "Cleaning node_modules..."
	rm -rf node_modules pnpm-lock.yaml apps/*/node_modules
	pnpm install

clean-all: clean clean-node
	@echo "All cleaned!"

.DEFAULT_GOAL := help
