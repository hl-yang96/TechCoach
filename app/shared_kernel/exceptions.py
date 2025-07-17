"""
Shared Exception Classes
File: app/shared_kernel/exceptions.py
Created: 2025-07-17
Purpose: Custom exception classes for consistent error handling across modules
"""

from typing import Any, Dict, Optional


class TechCoachException(Exception):
    """Base exception for all TechCoach-specific errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class DocumentProcessingException(TechCoachException):
    """Raised when document processing fails."""
    pass


class ValidationException(TechCoachException):
    """Raised when input validation fails."""
    pass


class RAGException(TechCoachException):
    """Raised when RAG operations fail."""
    pass


class LLMException(TechCoachException):
    """Raised when LLM operations fail."""
    pass


class VectorDBException(TechCoachException):
    """Raised when vector database operations fail."""
    pass


class SessionException(TechCoachException):
    """Raised when interview session operations fail."""
    pass


class NotFoundException(TechCoachException):
    """Raised when a requested resource is not found."""
    pass


class IngestionException(TechCoachException):
    """Raised when document ingestion fails."""
    pass


class RateLimitException(TechCoachException):
    """Raised when API rate limits are exceeded."""
    
    def __init__(self, message: str, limit: int, reset_time: Optional[int] = None):
        super().__init__(message)
        self.limit = limit
        self.reset_time = reset_time


class AuthenticationException(TechCoachException):
    """Raised when authentication fails."""
    pass


class ConfigurationException(TechCoachException):
    """Raised when configuration is invalid or missing."""
    pass