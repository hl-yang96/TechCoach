"""
Shared Kernel Module
File: app/shared_kernel/__init__.py
Created: 2025-07-17
Purpose: Common utilities, data models, and constants shared across modules
This module provides reusable components to avoid code duplication and ensure consistency.
"""

__module_name__ = "shared_kernel"
__description__ = "Shared utilities, models, and constants across modules"

from .constants import *
from .exceptions import *
from .validators import *