"""
Shared Data Models
File: app/shared_kernel/models.py
Created: 2025-07-17
Purpose: Common data structures and Pydantic models for type safety
Defines core entities like User, Document, InterviewSession, etc.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator


class DocumentType(str, Enum):
    """Types of supported documents for ingestion."""
    PDF = "pdf"
    MARKDOWN = "markdown"
    TEXT = "text"
    HTML = "html"
    DOCX = "docx"
    CODE = "code"
    JSON = "json"


class LLMProvider(str, Enum):
    """Available LLM providers for routing."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    AZURE = "azure"


class QuestionType(str, Enum):
    """Types of interview questions."""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"
    SITUATIONAL = "situational"


class SessionStatus(str, Enum):
    """Status of interview session."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


# Base Entity Models
class BaseEntity(BaseModel):
    """Base model for all entities with common attributes."""
    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class User(BaseEntity):
    """User entity representing a person using the coaching service."""
    username: str
    email: str
    career_goal: str = ""
    target_roles: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    years_experience: int = 0
    completed_sessions: int = 0


class Document(BaseEntity):
    """Represents a document ingested into the system."""
    user_id: str
    filename: str
    original_path: str
    document_type: DocumentType
    file_size: int
    content_hash: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_processed: bool = False

    @validator('document_type', pre=True)
    def validate_document_type(cls, v):
        if isinstance(v, str):
            return DocumentType(v.lower())
        return v


class Question(BaseEntity):
    """Represents an interview question."""
    title: str
    content: str
    category: QuestionType
    difficulty: str = Field("medium", regex=r"^easy|medium|hard$")
    topics: List[str] = Field(default_factory=list)
    expected_answer_points: List[str] = Field(default_factory=list)
    context_references: List[str] = Field(default_factory=list)


class InterviewSession(BaseEntity):
    """Represents an active interview session."""
    user_id: str
    job_description_id: Optional[str] = None
    status: SessionStatus = SessionStatus.PENDING
    questions: List[str] = Field(default_factory=list)  # Question IDs
    current_question_index: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    overall_score: Optional[float] = None


class QuestionResponse(BaseEntity):
    """Represents a user's response to a question."""
    session_id: str
    question_id: str
    user_response: str
    ai_feedback: Optional[str] = None
    scores: Dict[str, float] = Field(default_factory=dict)
    improvement_suggestions: List[str] = Field(default_factory=list)
    time_taken: Optional[int] = None  # seconds


class CareerDocument(BaseEntity):
    """Represents a career document like resume or cover letter."""
    user_id: str
    document_type: str = "resume"
    original_content: str
    optimized_content: Optional[str] = None
    target_job_id: Optional[str] = None
    focus_areas: List[str] = Field(default_factory=list)
    is_optimized: bool = False


# Request/Response Models
class DocumentUploadResponse(BaseModel):
    """Response for document upload operations."""
    document_id: str
    filename: str
    status: str
    processing_id: Optional[str] = None


class QuestionGenerationRequest(BaseModel):
    """Request for generating interview questions."""
    topic: str
    difficulty: str = "medium"
    number: int = Field(5, ge=1, le=20)
    include_context: bool = False


class ResumeAnalysisRequest(BaseModel):
    """Request for resume analysis against job description."""
    resume_text: str
    job_description: str
    target_company: Optional[str] = None


class ResumeAnalysisResponse(BaseModel):
    """Response for resume analysis."""
    analysis_id: str
    gap_analysis: List[Dict[str, Any]]
    suggested_bullets: List[str]
    overall_score: float
    recommendations: List[str]


# Vector similarity models
class SimilarDocument(BaseModel):
    """Result from vector similarity search."""
    document_id: str
    score: float
    content_preview: str
    metadata: Dict[str, Any]


class SearchQuery(BaseModel):
    """Vector search query."""
    query: str
    limit: int = Field(5, ge=1, le=50)
    filters: Optional[Dict[str, Any]] = None