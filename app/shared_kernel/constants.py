"""
Shared Constants and Configuration
File: app/shared_kernel/constants.py
Created: 2025-07-17
Purpose: Global constants and configuration values used across modules
"""

from __future__ import annotations

# Application Configuration
APP_NAME = "TechCoach"
APP_VERSION = "0.1.0"
API_PREFIX = "/api"

# Document Processing
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".txt": "text",
    ".md": "markdown",
    ".docx": "docx",
    ".html": "html",
    ".py": "code",
    ".js": "code",
    ".java": "code",
    ".cpp": "code",
    ".go": "code",
    ".rs": "code",
}

# Chunking Configuration
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# LLM Configuration
LLM_TIMEOUT = 30  # seconds
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# LLM Providers and Models
SUPPORTED_PROVIDERS = {
    "openai": {
        "models": [
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ],
        "embeddings": "text-embedding-3-small"
    },
    "anthropic": {
        "models": [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022"
        ]
    }
}

# Vector Database Configuration
CHROMA_COLLECTION_NAME = "techcoach_knowledge"
CHROMA_DISTANCE_FUNCTION = "cosine"

# Search Configuration
DEFAULT_SEARCH_LIMIT = 5
MAX_SEARCH_LIMIT = 50
MIN_SEARCH_SCORE = 0.7

# Interview Configuration
MAX_SESSION_QUESTIONS = 20
SESSION_TIMEOUT_MINUTES = 60
QUESTION_RETRIES = 3

# Scoring Configuration
SCORING_RANGES = {
    "clarity": (1, 5),
    "technical_accuracy": (1, 5),
    "completeness": (1, 5),
    "depth": (1, 5),
    "communication": (1, 5)
}

# File Storage Configuration
CONTENT_STORAGE_PATH = "app_data/content"
DOCUMENTS_STORAGE_PATH = "app_data/documents"
LOGS_STORAGE_PATH = "logs"

# Error Messages
ERROR_MESSAGES = {
    "FILE_TOO_LARGE": f"File size exceeds {MAX_FILE_SIZE/(1024*1024):.0f}MB limit",
    "UNSUPPORTED_FORMAT": "File format not supported",
    "DOCUMENT_NOT_FOUND": "Document not found",
    "SESSION_NOT_FOUND": "Interview session not found",
    "INVALID_QUESTION": "Invalid question format",
    "LLM_ERROR": "AI processing error occurred",
    "VECTOR_DB_ERROR": "Knowledge base connection error",
}

# Logging Configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# API Rate Limits
RATE_LIMIT_DEFAULT = 100
RATE_LIMIT_ANNOTATIONS = 50
RATE_LIMIT_TRANSLATION = 20

# Content Length Limits
MAX_RESUME_LENGTH = 5000  # characters
MAX_JD_LENGTH = 3000  # characters
MAX_ANSWER_LENGTH = 2000  # characters
MAX_QUESTION_LENGTH = 500  # characters

# Encoding for various text types
ENCODING = "utf-8"