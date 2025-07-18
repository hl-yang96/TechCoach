"""
TechCoach - Centralized Database Configuration
File: shared_kernel/database.py
Module: Database
Purpose: Centralized database connection and initialization for SQLModel + SQLite
Provides: Database session management, connection setup, and initialization utilities
"""

import os
from pathlib import Path
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy import text

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"sqlite:///{Path(__file__).parent.parent.parent}/app_data/techcoach.db"
)

# Global session factory
_engine = None
_session_factory = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        # Configure SQLite for thread safety with FastAPI
        connect_args = {"check_same_thread": False}
        _engine = create_engine(
            DATABASE_URL,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",  # Enable query logging in dev
            poolclass=StaticPool,
            connect_args=connect_args,
        )
    return _engine


def get_session() -> Generator[Session, None, None]:
    """Yield database session for FastAPI dependency injection."""
    engine = get_engine()
    with Session(engine) as session:
        yield session


def init_database():
    """Initialize database - create tables based on SQLModel models."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    

def get_session_factory():
    """Get session factory for manual session management."""
    global _session_factory
    if _session_factory is None:
        engine = get_engine()
        _session_factory = Session(engine)
    return _session_factory


def close_fixtures():
    """Clean up database connections (shutdown hook)."""
    global _engine, _session_factory
    if _session_factory:
        _session_factory.close()
        _session_factory = None
    if _engine:
        _engine.dispose()
        _engine = None


# FastAPI dependency injection
async def get_db():
    """Async dependency for FastAPI - yields database session."""
    with Session(get_engine()) as session:
        try:
            yield session
        finally:
            session.close()


# Health check function
def check_database():
    """Health check for database connectivity."""
    try:
        engine = get_engine()
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connectivity check failed: {e}")
        return False