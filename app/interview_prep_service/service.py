"""
Interview Service
File: app/interview/service.py
Created: 2025-07-17
Purpose: Core interview logic with AI integration
"""

from typing import List, Dict
from uuid import uuid4

from ..shared_kernel.models import Question, QuestionType, InterviewSession


class InterviewService:
    """Service for managing interview workflows."""
    
    # def __init__(self):