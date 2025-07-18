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
