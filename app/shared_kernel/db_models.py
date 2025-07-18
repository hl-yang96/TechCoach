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
from enum import Enum


# ===== BASE ENTITY =====

class BaseDBModel(SQLModel):
    """Base database model with common fields."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ===== ENUM TYPES FOR DATABASE =====

class DifficultyLevel(str, Enum):
    """Question difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class QuestionStatus(str, Enum):
    """Question processing status."""
    PENDING = "pending"
    GENERATED = "generated"
    REVIEWED = "reviewed"
    ARCHIVED = "archived"


class UserRole(str, Enum):
    """User roles for access control."""
    BASIC = "basic"
    PREMIUM = "premium"
    ADMIN = "admin"


# ===== TODO: FUTURE DATABASE TABLES =====

# TODO: Interview Question Storage
# class InterviewQuestion(BaseDBModel, table=True):
#     """Individual interview questions with full metadata."""
#     __tablename__ = "interview_questions"
#     
#     # Core content
#     question_text: str
#     category: str = Field(index=True)
#     difficulty: DifficultyLevel = Field(index=True)
#     expected_topics: Optional[str] = None  # JSON array
#     
#     # User context
#     target_role: Optional[str] = None
#     company_focus: Optional[str] = None
#     
#     # Metadata
#     usage_count: int = Field(default=0, index=True)
#     correct_answer_count: int = Field(default=0)
#     avg_response_time: Optional[float] = None
#     quality_score: Optional[float] = None
#     created_by: str = Field(default="system")
#     tags: Optional[str] = None  # JSON array


# TODO: User Session Management  
# class UserSession(BaseDBModel, table=True):
#     """Persistent user session data."""
#     __tablename__ = "user_sessions"
#     
#     session_id: str = Field(unique=True, index=True)
#     user_preferences: Optional[str] = None  # JSON
#     career_goals: Optional[str] = None
#     active_categories: Optional[str] = None  # JSON array
#     session_metadata: Optional[str] = None  # JSON object
#     is_active: bool = Field(default=True, index=True)


# TODO: Practice History
# class PracticeRecord(BaseDBModel, table=True):
#     """History of practice sessions and answers."""
#     __tablename__ = "practice_records"
#     
#     session_id: str = Field(index=True)
#     question_id: int = Field(index=True)  # foreign key to questions
#     user_response: str
#     is_correct: Optional[bool] = None
#     feedback_received: Optional[str] = None
#     time_spent: Optional[int] = None  # in seconds
#     confidence_level: Optional[int] = None  # 1-10 scale
#     retry_count: int = Field(default=0)


# TODO: Chat History and Messages
# class ChatMessage(BaseDBModel, table=True):
#     """AI chat conversations and messages."""
#     __tablename__ = "chat_messages"
#     
#     session_id: str = Field(index=True)
#     role: str = Field(index=True)  # 'user', 'assistant', 'system'
#     content: str  
#     message_type: str = Field(default="text")  # text, question, feedback
#     category_context: Optional[str] = None
#     timestamp: datetime = Field(default_factory=datetime.utcnow)
#     metadata: Optional[str] = None  # JSON for additional context


# TODO: User Progress Tracking
# class ProgressMetrics(BaseDBModel, table=True):
#     """Aggregated progress metrics per category/user."""
#     __tablename__ = "progress_metrics"
#     
#     session_id: str = Field(index=True)
#     category: str = Field(index=True)
#     total_questions: int = Field(default=0)
#     correct_answers: int = Field(default=0)
#     avg_confidence: Optional[float] = None
#     mastery_level: str = Field(default="beginner")
#     last_practiced: Optional[datetime] = None
#     streak_days: int = Field(default=0)


# TODO: Document Analysis Results
# class DocumentAnalysis(BaseDBModel, table=True):
#     """Analysis of uploaded career documents."""
#     __tablename__ = "document_analyses"
#     
#     session_id: str = Field(index=True)
#     document_type: str = Field(index=True)  # resume, cover_letter, etc.
#     original_content_hash: str = Field(unique=True)  # Deduplication
#     analysis_result: str  # JSON object
#     improvement_suggestions: Optional[str] = None  # JSON array
#     confidence_score: Optional[float] = None


# ===== INITIALIZATION TABLE =====

class SchemaVersion(BaseDBModel, table=True):
    """Track database schema version for migrations."""
    __tablename__ = "schema_versions"
    
    version: str = Field(unique=True, index=True)
    description: str
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    is_current: bool = Field(default=True, index=True)


# ===== UTILITY MODELS FOR FUTURE USE =====

# class DatabaseHealth(BaseDBModel):
#     """Database health check entity."""
#     
#     health_check_key: str = Field(unique=True)
#     last_check: datetime
#     status: str
#     details: Optional[str] = None