"""
Career Documents Router
File: app/gateway/routers/career_docs.py
Created: 2025-07-17
Purpose: Resume optimization and career document management endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any, List

router = APIRouter()
