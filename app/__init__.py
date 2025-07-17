"""
TechCoach Application Core
File: app/__init__.py
Created: 2025-07-17
Purpose: Main application package initialization for TechCoach AI career coaching platform
This package implements the modular monolith architecture with clear module boundaries.
"""

__version__ = "0.1.0"
__author__ = "TechCoach Dev Team"
__description__ = "AI-powered personalized career coaching platform"

# Expose main application
from .main import app

__all__ = ["app"]