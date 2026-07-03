import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "WelvoxAgent"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://welvox:welvox_dev_password@localhost:5432/welvox_ai"
    )
    DATABASE_ECHO: bool = DEBUG
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_CACHE_TIMEOUT: int = 3600  # 1 hour
    
    # Vector Database (Qdrant)
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION_NAME: str = "welvox_embeddings"
    
    # AI Providers
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    
    # Default Models
    DEFAULT_MODEL: str = "claude-3-5-sonnet-20241022"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Authentication
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")
    CLERK_API_KEY: str = os.getenv("CLERK_API_KEY", "")
    
    # Tool Integrations
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GMAIL_CREDENTIALS: str = os.getenv("GMAIL_CREDENTIALS", "")
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")
    NOTION_API_TOKEN: str = os.getenv("NOTION_API_TOKEN", "")
    DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
    FIGMA_API_TOKEN: str = os.getenv("FIGMA_API_TOKEN", "")
    JIRA_API_TOKEN: str = os.getenv("JIRA_API_TOKEN", "")
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
    
    # Feature Flags
    ENABLE_STREAMING: bool = True
    ENABLE_MEMORY: bool = True
    ENABLE_RAG: bool = True
    ENABLE_BACKGROUND_JOBS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True


settings = Settings()
