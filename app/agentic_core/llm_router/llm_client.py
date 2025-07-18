"""
TechCoach - LangChain LLM Client
File: agentic_core/llm_router/llm_client.py
Purpose: Simple LangChain-based LLM client for single provider
Supports: kimi, openai, claude, gemini, deepseek
"""

import os
from typing import Optional, Dict, Any
import yaml
from pathlib import Path
from pydantic import BaseModel
from enum import Enum

# LangChain imports - use updated package-specific imports to avoid deprecation warnings
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

class LLMProvider(str, Enum):
    """Supported LLM providers for TechCoach."""
    KIMI = "kimi"
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"


class LLMConfig(BaseModel):
    """Simple LLM configuration model."""
    provider: str
    api_key: str
    model: str
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000


class LLMClient:
    """Single LLM provider client using LangChain."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.client = self._create_client()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration path."""
        project_root = Path(__file__).parent.parent.parent.parent
        return str(project_root / "config" / "llm_config.yaml")
    
    def _load_config(self) -> LLMConfig:
        """Load configuration from YAML."""
        try:
            config_path = Path(self.config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"LLM config not found at {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # Get selected provider
            provider = config_data.get('provider', 'kimi')
            provider_config = config_data['providers'][provider]
            
            # Get API key from config or environment
            api_key = provider_config.get('api_key')
            if not api_key:
                env_mapping = {
                    'kimi': 'KIMI_API_KEY',
                    'openai': 'OPENAI_API_KEY',
                    'claude': 'ANTHROPIC_API_KEY',
                    'gemini': 'GEMINI_API_KEY',
                    'deepseek': 'DEEPSEEK_API_KEY'
                }
                api_key = os.getenv(env_mapping.get(provider, ''))
            
            if not api_key:
                raise ValueError(f"No API key found for provider {provider}")
            
            return LLMConfig(
                provider=provider,
                api_key=api_key,
                model=provider_config.get('model'),
                api_base=provider_config.get('api_base'),
                temperature=config_data.get('temperature', 0.7),
                max_tokens=config_data.get('max_tokens', 2000)
            )
            
        except Exception as e:
            print(f"Error loading LLM config: {e}")
            raise
    
    def _create_client(self):
        """Create LangChain client for the configured provider."""
        config = self.config

        if config.provider == 'claude':
            return ChatAnthropic(
                api_key=config.api_key,
                model_name=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens
                # Note: Claude doesn't use top_p parameter, it's handled internally
            )
        elif config.provider == 'gemini':
            return ChatGoogleGenerativeAI(
                google_api_key=config.api_key,
                model=config.model,
                temperature=config.temperature,
                max_output_tokens=config.max_tokens
            )
        else:
            return ChatOpenAI(
                api_key=config.api_key,
                model=config.model,
                base_url=config.api_base,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
    
    def chat(self, message: str) -> str:
        """Send a chat message and get response."""
        try:
            response = self.client.invoke(message)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_config(self) -> LLMConfig:
        """Get current configuration."""
        return self.config


# Global LLM client instance
_llm_client = LLMClient()

def get_llm_client() -> LLMClient:
    """Get or create singleton LLM client."""
    return _llm_client