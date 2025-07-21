"""
TechCoach - SQLModel Database Models Framework
File: shared_kernel/db_models.py
Module: Database Models (SQLModel)
Purpose: SQLModel-based database models for persistent storage
Status: Framework only - Placeholder structure for future implementation
Usage: Centralized database models for non-vector data storage
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TechDomainEntity():
    name: str
    def __init__(self, name: str):
        self.name = name


class TechDomainQuestionEntity():
    """Tech Domain Question Entity"""
    def __init__(
        self,
        id: int,
        domain_name: str,
        question_text: str,
        user_answer: Optional[str] = None,
        generated_answer: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.domain_name = domain_name
        self.question_text = question_text
        self.user_answer = user_answer
        self.generated_answer = generated_answer
        self.created_at = created_at
        self.updated_at = updated_at


class DocumentEntity():
    """Document Entity for uploaded documents"""
    def __init__(
        self,
        id: str,
        filename: str,
        file_path: str,
        collection_type: str,
        chroma_document_id: Optional[str] = None,
        is_local_file: bool = True,
        file_size: Optional[int] = None,
        content_preview: Optional[str] = None,
        upload_method: str = "file",  # "file" or "text"
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.filename = filename
        self.file_path = file_path
        self.collection_type = collection_type
        self.chroma_document_id = chroma_document_id
        self.is_local_file = is_local_file
        self.file_size = file_size
        self.content_preview = content_preview
        self.upload_method = upload_method
        self.created_at = created_at
        self.updated_at = updated_at
