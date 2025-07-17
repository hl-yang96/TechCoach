"""
TechCoach Main Application Entry Point
File: app/main.py
Created: 2025-07-17
Purpose: Main FastAPI application for TechCoach AI career coaching platform
Entry point for the modular monolith architecture
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import application routers
from app.gateway.routers.health import router as health_router
from app.gateway.routers.document import router as document_router
from app.gateway.routers.interview import router as interview_router
from app.gateway.routers.career_docs import router as career_docs_router

# Import middleware
from app.gateway.middleware.logging import RequestLoggingMiddleware
from app.gateway.middleware.error_handler import ErrorHandlerMiddleware


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="TechCoach API",
        description="AI-powered personalized career coaching platform",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://frontend:80"],
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

    return app


# Create the FastAPI application
app = create_app()


@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    import os
    from app.agentic_core.core import initialize_ai_systems
    
    # Initialize AI systems (RAG, LLM routing, etc.)
    await initialize_ai_systems()
    
    print("TechCoach API started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    print("TechCoach API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8001,
        reload=True,
        log_level="info"
    )