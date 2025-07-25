"""
TechCoach - Multi-Provider LLM Integration Module
Package: agentic_core/llm_router
Purpose: Multi-provider LLM interface using LangChain for AI career coaching
Features:
- Multi-provider support via configuration
- LangChain and CrewAI unified interface
- Provider-specific client management
- Easy configuration via YAML with environment fallback
- Support for different client types (default, agent_process, tool_call, content)
"""

from .llm_client import (
    LLMClientManager,
    LLMConfig,
    ProviderConfig,
    MultiProviderConfig,
    LLMProvider,
    get_llm_client_manager,
)

# Re-export main components
__all__ = [
    'LLMClientManager',
    'LLMConfig',
    'ProviderConfig',
    'MultiProviderConfig',
    'LLMProvider',
    'get_llm_client_manager',
]

# Version info
__version__ = "0.3.0"