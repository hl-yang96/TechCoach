"""
Interview Management Router
File: app/gateway/routers/interview.py
Created: 2025-07-17
Purpose: Interview session management and question generation endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from uuid import uuid4

router = APIRouter()

