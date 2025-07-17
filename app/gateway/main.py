"""
FastAPI Application Entry Point
File: app/gateway/main.py
Created: 2025-07-17
Purpose: Main FastAPI application configuration, routers, and middleware setup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Import routers
from .routers.health import router as health_router
from .routers.document import router as document_router
from .routers.interview import router as interview_router
from .routers.career_docs import router as career_docs_router

# Import middleware
from .middleware.error_handler import ErrorHandler
from .middleware.logging import RequestLoggingMiddleware

# Create FastAPI instance
def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="TechCoach API",
        description="AI-powered personalized career coaching platform",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Add middleware
    app.add_middleware(ErrorHandler)
    app.add_middleware(RequestLoggingMiddleware)

    # Include routers
    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(document_router, prefix="/api/documents", tags=["documents"])
    app.include_router(interview_router, prefix="/api/interview", tags=["interview"])
    app.include_router(career_docs_router, prefix="/api/career", tags=["career"])

    return app

# Create the application
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)