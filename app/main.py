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

# Import LLM integration  
from app.agentic_core.llm_router.llm_client import get_llm_client

import logging

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
    
    # Initialize LLM configuration for questions
    try:
        # Initialize LLM test
        await _initialize_llm_test()
    except Exception as e:
        print(f"⚠️ LLM configuration warning: {e}")
    
    # Initialize question service
    try:
        from app.question_service.service import tech_domain_service
        print("✅ Question service initialized")
    except Exception as e:
        print(f"⚠️ Question service initialization warning: {e}")
    
    # Yield control to FastAPI
    yield
    
    # Shutdown
    print("🛑 TechCoach API shutting down...")

async def _initialize_llm_test():
    """Send initial test request to verify LLM functionality."""
    try:
        print("🧪 Initializing LLM test...")
        
        # Get LLM client
        llm_client = get_llm_client()
        config = llm_client.get_config()
        
        if not config.api_key:
            print("⚠️ No API key configured for LLM")
            print("Please check config/llm_config.yaml or set relevant environment variables")
            return
            
        # Test the client
        print(f"🎯 Testing LLM with {config.provider}...")
        response = llm_client.chat("Hello, please confirm you can respond.")
        
        if "Error:" in response:
            print(f"❌ LLM Test Failed: {response}")
        else:
            print("✅ LLM Test Success!")
            print(f"   Provider: {config.provider}")
            print(f"   Model: {config.model}")
            print(f"   Response: {response.strip()}")
            
    except Exception as e:
        print(f"❌ LLM Test Failed: {e}")
        print(f"   This is expected if no API keys are configured yet")
        print(f"   Please set up config/llm_config.yaml")
        raise e


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
    from app.gateway.routers.question import router as question_router
    
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(document_router, prefix="/api/documents", tags=["Documents"])
    app.include_router(interview_router, prefix="/api/interview", tags=["Interview"])
    app.include_router(career_docs_router, prefix="/api/career", tags=["Career"])
    app.include_router(question_router, prefix="/api/questions", tags=["Questions"])

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