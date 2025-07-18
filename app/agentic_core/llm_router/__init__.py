"""
TechCoach - LangChain LLM Integration Module
Package: agentic_core/llm
Purpose: Simplified LLM interface using LangChain for AI career coaching
Features:
- Single provider support via configuration
- LangChain-based unified interface
- Simple chat functionality
- Easy configuration via YAML with environment fallback
"""

from .llm_client import (
    LLMClient,
    LLMConfig,
    get_llm_client,
    LLMProvider
)

# Re-export main components
__all__ = [
    'LLMClient',
    'LLMConfig',
    'get_llm_client',
    'LLMProvider'
]

# Version info
__version__ = "0.2.0"