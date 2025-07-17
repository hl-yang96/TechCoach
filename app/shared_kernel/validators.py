"""
Shared Validation Utilities
File: app/shared_kernel/validators.py
Created: 2025-07-17
Purpose: Reusable validation functions for input sanitization and data validation
"""

from __future__ import annotations
from pathlib import Path
from typing import Union, Optional
import mimetypes

from .constants import SUPPORTED_EXTENSIONS, MAX_FILE_SIZE, MAX_RESUME_LENGTH, MAX_JD_LENGTH
from .exceptions import ValidationException


def validate_file_size(file_size: int, max_size: int = MAX_FILE_SIZE) -> None:
    """
    Validate file size doesn't exceed maximum allowed.
    
    Args:
        file_size: Size of file in bytes
        max_size: Maximum allowed size in bytes
    
    Raises:
        ValidationException: If file size exceeds limit
    """
    if file_size > max_size:
        raise ValidationException(
            f"File size {file_size} exceeds maximum allowed size {max_size}"
        )


def validate_file_extension(filename: str) -> str:
    """
    Validate file extension is supported.
    
    Args:
        filename: Original filename
    
    Returns:
        Document type as string
    
    Raises:
        ValidationException: If extension is not supported
    """
    path = Path(filename.lower())
    extension = path.suffix
    
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValidationException(
            f"Unsupported file extension: {extension}. Supported: {list(SUPPORTED_EXTENSIONS.keys())}"
        )
    
    return SUPPORTED_EXTENSIONS[extension]


def validate_mime_type(content_type: str, expected_types: set[str]) -> bool:
    """
    Validate content type (MIME type).
    
    Args:
        content_type: Content type from HTTP headers
        expected_types: Set of expected MIME types
    
    Returns:
        True if valid
    
    Raises:
        ValidationException: If MIME type is invalid
    """
    if content_type not in expected_types:
        raise ValidationException(
            f"Invalid content type: {content_type}. Expected: {expected_types}"
        )
    return True


def validate_text_length(text: str, max_length: int, field_name: str = "Text") -> str:
    """
    Validate text length doesn't exceed maximum.
    
    Args:
        text: Text to validate
        max_length: Maximum allowed length
        field_name: Name of field for error messages
    
    Returns:
        Sanitized text
    
    Raises:
        ValidationException: If text is too long
    """
    if len(text) > max_length:
        raise ValidationException(
            f"{field_name} length {len(text)} exceeds maximum {max_length}"
        )

    return text.strip()


def validate_resume_text(resume_text: str) -> str:
    """Validate resume text content and length."""
    return validate_text_length(resume_text, MAX_RESUME_LENGTH, "Resume text")


def validate_job_description(job_description: str) -> str:
    """Validate job description text content and length."""
    return validate_text_length(job_description, MAX_JD_LENGTH, "Job description")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = Path(filename).name
    
    # Remove illegal characters
    import re
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Ensure file has extension
    if not filename:
        filename = "document"
    
    # Limit length
    max_length = 200
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = f"{name[:max_length-len(ext)-1]}.{ext}" if ext else name[:max_length]
    
    return filename


def validate_question_count(count: int, min_val: int = 1, max_val: int = 20) -> int:
    """
    Validate question count for generation.
    
    Args:
        count: Number of questions requested
        min_val: Minimum questions
        max_val: Maximum questions
    
    Returns:
        Valid count
    
    Raises:
        ValidationException: If count is out of range
    """
    if not isinstance(count, int):
        raise ValidationException("Question count must be an integer")
    
    if count < min_val or count > max_val:
        raise ValidationException(
            f"Question count {count} must be between {min_val} and {max_val}"
        )
    
    return count


class TemplateValidator:
    """Validates template and prompt arguments."""
    
    @staticmethod
    def validate_context_variables(context: dict, required_vars: set[str]) -> None:
        """
        Validate context contains all required variables.
        
        Args:
            context: Template context dictionary
            required_vars: Set of required variable names
        
        Raises:
            ValidationException: If required variables are missing
        """
        missing_vars = required_vars - set(context.keys())
        if missing_vars:
            raise ValidationException(
                f"Missing required context variables: {missing_vars}"
            )