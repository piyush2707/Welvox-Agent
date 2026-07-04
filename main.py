"""
WelvoxAgent FastAPI Backend
Universal AI Operating System - One AI. Infinite Skills.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="WelvoxAgent API",
    description="Universal AI Operating System API",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://welvox.ai",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "SERVER_ERROR",
                "message": "An internal server error occurred",
            },
        },
    )


# Root endpoint welcome message
@app.get("/")
def home():
    return {"message": "Welcome to Welvox Agent! The system is up and running successfully."}

@app.get("/health")
async def health():
    
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


# Initialize endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("WelvoxAgent API starting up...")
    # Initialize database, cache, vector store, etc.


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("WelvoxAgent API shutting down...")


# Include routers
# These will be created in separate files
logger.info("WelvoxAgent API initialized successfully")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development",
    )
