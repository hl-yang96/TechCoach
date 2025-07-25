"""
TechCoach - Multi-Provider LLM Client
File: agentic_core/llm_router/llm_client.py
Purpose: Multi-provider LLM client supporting multiple providers simultaneously
Supports: All providers defined in llm_config.yaml
"""

import os, sys
from typing import Optional, Dict, Any, Union
import logging
import yaml
from pathlib import Path
from pydantic import BaseModel
from enum import Enum

# LangChain imports - use updated package-specific imports to avoid deprecation warnings
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

from crewai import LLM

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    # Special provider types for different use cases
    DEFAULT = "default"
    AGENT_PROCESS = "agent_process"
    TOOL_CALL = "tool_call"
    CONTENT = "content"


class LLMConfig(BaseModel):
    provider: str
    api_key: str
    model: str
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 8192
    api_key_env: Optional[str] = None


class ProviderConfig(BaseModel):
    """Configuration for a single provider"""
    api_key: Optional[str] = None
    api_key_env: Optional[str] = None
    model: str
    api_base: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class MultiProviderConfig(BaseModel):
    """Configuration for multiple providers"""
    provider: Dict[str, str]  # default, agent_process, tool_call, content
    setting: Dict[str, Any]   # global settings
    providers: Dict[str, ProviderConfig]  # provider-specific configs


class LLMClientManager:
    """Multi-provider LLM client that can manage multiple LLM instances"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.multi_config = self._load_multi_config()
        self.provider_clients = {}  # Cache for provider clients
        self.provider_crew_clients = {}  # Cache for crew clients

        # Initialize default clients for backward compatibility
        default_provider = self.multi_config.provider.get("default")
        if default_provider:
            self.config = self._get_provider_config(default_provider)  # Set config for backward compatibility
            self.client = self._create_client_for_provider(default_provider)
            self.crew_client = self._create_crew_client_for_provider(default_provider)
        else:
            self.config = None
            self.client = None
            self.crew_client = None

    def _get_default_config_path(self) -> str:
        project_root = Path(__file__).parent.parent.parent.parent
        return str(project_root / "config" / "llm_config.yaml")

    def _load_multi_config(self) -> MultiProviderConfig:
        try:
            config_path = Path(self.config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"LLM config not found at {config_path}")

            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)

            # Parse provider configurations
            providers = {}
            for provider_name, provider_data in config_data.get('providers', {}).items():
                providers[provider_name] = ProviderConfig(**provider_data)

            return MultiProviderConfig(
                provider=config_data.get('provider', {}),
                setting=config_data.get('setting', {}),
                providers=providers
            )

        except Exception as e:
            print(f"Error loading LLM config: {e}")
            raise
    
    def _get_api_key_for_provider(self, provider_name: str) -> str:
        """Get API key for a specific provider"""
        provider_config = self.multi_config.providers.get(provider_name)
        if not provider_config:
            raise ValueError(f"Provider {provider_name} not found in config")

        # First try the api_key from config
        api_key = provider_config.api_key
        if api_key:
            return api_key

        # Then try from environment using api_key_env
        if provider_config.api_key_env:
            api_key = os.getenv(provider_config.api_key_env)
            if api_key:
                return api_key

        raise ValueError(f"No API key found for provider {provider_name}")

    def _get_provider_config(self, provider_name: str) -> LLMConfig:
        """Get complete configuration for a specific provider"""
        provider_config = self.multi_config.providers.get(provider_name)
        if not provider_config:
            raise ValueError(f"Provider {provider_name} not found in config")

        api_key = self._get_api_key_for_provider(provider_name)

        # Use provider-specific settings or fall back to global settings
        global_settings = self.multi_config.setting
        temperature = provider_config.temperature or global_settings.get('temperature', 0.7)
        max_tokens = provider_config.max_tokens or global_settings.get('max_tokens', 8192)

        return LLMConfig(
            provider=provider_name,
            api_key=api_key,
            model=provider_config.model,
            api_base=provider_config.api_base,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key_env=provider_config.api_key_env
        )

    def _create_client_for_provider(self, provider_name: str):
        """Create a LangChain client for a specific provider"""
        config = self._get_provider_config(provider_name)

        # Cache the client
        if provider_name in self.provider_clients:
            return self.provider_clients[provider_name]

        if config.provider == 'claude':
            client = ChatAnthropic(
                api_key=config.api_key,
                model_name=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens
                # Note: Claude doesn't use top_p parameter, it's handled internally
            )
        elif config.provider == 'gemini':
            client = ChatGoogleGenerativeAI(
                google_api_key=config.api_key,
                model=config.model,
                temperature=config.temperature,
                max_output_tokens=config.max_tokens
            )
        else:
            # Default to OpenAI-compatible API for all other providers
            client = ChatOpenAI(
                api_key=config.api_key,
                model=config.model,
                base_url=config.api_base,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
        logger.info(f"Created client for provider: {provider_name}, model: {config.model}, temperature: {config.temperature}, max_tokens: {config.max_tokens}")
        self.provider_clients[provider_name] = client
        return client
    
    def _create_crew_client_for_provider(self, provider_name: str):
        """Create a CrewAI LLM client for a specific provider"""
        config = self._get_provider_config(provider_name)
        # Cache the client
        if provider_name in self.provider_crew_clients:
            return self.provider_crew_clients[provider_name]
        # create CrewAI client
        model = "openai/" + config.model if config.provider != 'claude' else "anthropic/" + config.model
        client = LLM(
                model=model, base_url=config.api_base, api_key=config.api_key,
                temperature=config.temperature, max_tokens=config.max_tokens
            )

        self.provider_crew_clients[provider_name] = client
        return client

    def chat(self, message: str, provider: Optional[Union[str, LLMProvider]] = None) -> str:
        """Chat using specified provider or default"""
        try:
            if provider:
                provider_name = provider.value if isinstance(provider, LLMProvider) else provider
                client = self._create_client_for_provider(provider_name)
            else:
                client = self.client

            if not client:
                raise ValueError("No client available")

            response = client.invoke(message)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def get_client(self, provider: Union[str, LLMProvider]):
        """Get LangChain client for specific provider"""
        provider_name = provider.value if isinstance(provider, LLMProvider) else provider
        return self._create_client_for_provider(provider_name)

    def get_crew_client(self, provider: Union[str, LLMProvider]):
        """Get CrewAI client for specific provider"""
        provider_name = provider.value if isinstance(provider, LLMProvider) else provider
        return self._create_crew_client_for_provider(provider_name)

    def get_client_by_type(self, client_type: LLMProvider):
        """Get client by predefined type (DEFAULT, AGENT_PROCESS, TOOL_CALL, CONTENT)"""
        if client_type in [LLMProvider.DEFAULT, LLMProvider.AGENT_PROCESS,
                          LLMProvider.TOOL_CALL, LLMProvider.CONTENT]:
            provider_name = self.multi_config.provider.get(client_type.value)
            if provider_name:
                return self._create_client_for_provider(provider_name)

        raise ValueError(f"Invalid client type or no provider configured for {client_type}")

    def get_crew_client_by_type(self, client_type: LLMProvider):
        """Get CrewAI client by predefined type (DEFAULT, AGENT_PROCESS, TOOL_CALL, CONTENT)"""
        if client_type in [LLMProvider.DEFAULT, LLMProvider.AGENT_PROCESS,
                          LLMProvider.TOOL_CALL, LLMProvider.CONTENT]:
            provider_name = self.multi_config.provider.get(client_type.value)
            if provider_name:
                return self._create_crew_client_for_provider(provider_name)

        raise ValueError(f"Invalid client type or no provider configured for {client_type}")

    def get_config(self, provider: Optional[Union[str, LLMProvider]] = None) -> LLMConfig:
        """Get configuration for specific provider or default"""
        if provider:
            provider_name = provider.value if isinstance(provider, LLMProvider) else provider
            return self._get_provider_config(provider_name)
        elif hasattr(self, 'config'):
            return self.config
        else:
            default_provider = self.multi_config.provider.get("default")
            if default_provider:
                return self._get_provider_config(default_provider)
            raise ValueError("No default provider configured")

    def get_default_llm_client(self):
        """Backward compatibility method"""
        return self.client

    def get_default_crew_client(self):
        """Backward compatibility method"""
        return self.crew_client

    def list_available_providers(self) -> list:
        """List all available providers"""
        return list(self.multi_config.providers.keys())


# Global LLM client instance
_llm_client = None

def get_llm_client_manager() -> LLMClientManager:
    """Get or create singleton LLM client."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClientManager()
    return _llm_client
