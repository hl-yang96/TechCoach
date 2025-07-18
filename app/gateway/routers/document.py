"""
Document Management Router
File: app/gateway/routers/document.py
Created: 2025-07-17
Purpose: Document upload, processing, and retrieval endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from typing import List, Dict, Any

router = APIRouter()

