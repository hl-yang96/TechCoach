"""
TechCoach Main Application Entry Point
File: app/main.py
Created: 2025-07-17
Purpose: Main FastAPI application for TechCoach AI career coaching platform
Entry point for the modular monolith architecture (no warnings version)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database connection
from app.shared_kernel.database import init_database, check_database
from app.shared_kernel.db_models import SchemaVersion  # Ensure proper initialization

# Import application routers
from app.gateway.routers.health import router as health_router
from app.gateway.routers.document import router as document_router
from app.gateway.routers.interview import router as interview_router
from app.gateway.routers.career_docs import router as career_docs_router

# Import middleware
from app.gateway.middleware.logging import RequestLoggingMiddleware
from app.gateway.middleware.error_handler import ErrorHandlerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handlers for FastAPI."""
    # Startup
    print("🚀 TechCoach API starting...")
    
    # Initialize database
    try:
        print("📊 Initializing database...")
        init_database()
        
        if check_database():
            print("✅ Database initialized successfully")
        else:
            print("⚠️  Database connection check failed")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    
    yield
    # Shutdown
    print("👋 TechCoach API shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="TechCoach API",
        description="AI-powered personalized career coaching platform",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:4173",  # Vite preview
            "http://127.0.0.1:4173"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ErrorHandlerMiddleware)

    # Include routers
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(document_router, prefix="/api/documents", tags=["Documents"])
    app.include_router(interview_router, prefix="/api/interview", tags=["Interview"])
    app.include_router(career_docs_router, prefix="/api/career", tags=["Career"])

    # Simple root endpoint
    @app.get("/")
    async def root():
        return {"message": "Welcome to TechCoach API", "version": "0.1.0"}

    return app


# Create and export the FastAPI application
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8001,
        reload=True,
        log_level="info"
    )