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
        chroma_document_id_list: Optional[str] = None,  # JSON string of list
        file_size: Optional[int] = None,
        file_description: Optional[str] = None,
        file_abstract: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.filename = filename
        self.file_path = file_path
        self.collection_type = collection_type
        self.chroma_document_id_list = chroma_document_id_list
        self.file_size = file_size
        self.file_description = file_description
        self.file_abstract = file_abstract
        self.created_at = created_at
        self.updated_at = updated_at


        self.id
        self.filename
        self.file_path
        self.collection_type
        self.chroma_document_id_list
        self.file_size
        self.file_description
        self.file_abstract
        self.created_at
        self.updated_at
