"""
Document Processor for TechCoach RAG System
File: app/agentic_core/rag/document_classifier.py
Purpose: LLM-based document preprocessing including classification, cleaning, renaming, and metadata generation
"""

import json
import logging
from typing import Dict, Any

from ..llm_router.llm_client import LLMProvider, get_llm_client_manager
from .config import (
    DOCUMENT_PREPROCESSING_PROMPT,
    COLLECTION_CONFIGS,
    COLLECTION_RESUMES, COLLECTION_PROJECTS_EXPERIENCE, COLLECTION_JOB_POSTINGS
)

logger = logging.getLogger(__name__)


def _truncate_metadata(metadata: Dict[str, Any], max_field_length: int = 30) -> Dict[str, Any]:
    """
    Truncate metadata fields to prevent chunk size issues.

    Args:
        metadata: Original metadata dictionary
        max_field_length: Maximum length for each field

    Returns:
        Truncated metadata dictionary
    """
    truncated = {}

    for key, value in metadata.items():
        if isinstance(value, str):
            # Truncate string values
            truncated[key] = value[:max_field_length] if len(value) > max_field_length else value
        elif isinstance(value, list):
            # Truncate list items and limit list length
            truncated_list = []
            for item in value[:5]:  # Limit to 5 items
                if isinstance(item, str):
                    truncated_list.append(item[:20] if len(item) > 20 else item)
                else:
                    truncated_list.append(item)
            truncated[key] = truncated_list
        else:
            # Keep other types as is
            truncated[key] = value

    return truncated


class DocumentProcessor:
    """
    LLM-based document processor for comprehensive document preprocessing.

    This class uses the LLM router to perform all preprocessing tasks in a single LLM call:
        rename: rename the document to a meaningful name, even if filename is provided
        description: generate a brief description of the document, about 20~30 characters
        abstract: give a brief summary of the document, about 80~100 characters
        cleaning: remove special characters and format, normalize text
        classification: determine the appropriate collection type
    """

    def __init__(self):
        """Initialize the document processor."""
        self.llm_client = get_llm_client_manager()
        
    def process_document(self, document_content: str, filename: str = "") -> Dict[str, Any]:
        """
        Comprehensive document preprocessing including rename, description, abstract, cleaning, and classification.

        Args:
            document_content: The content of the document to process
            filename: Optional filename for additional context

        Returns:
            Dictionary containing all preprocessing results:
            - renamed_filename: Generated meaningful filename
            - description: Brief description (20-30 chars)
            - abstract: Detailed summary (80-100 chars)
            - cleaned_content: Normalized text content
            - collection_type: Determined collection type
            - metadata: Enhanced metadata
            - confidence: Classification confidence
            - reasoning: Classification reasoning
        """
        try:
            # Prepare the prompt with new preprocessing prompt
            prompt = DOCUMENT_PREPROCESSING_PROMPT.format(
                document_content=document_content,  # Increased limit for better processing
                filename=filename or "未知"
            )
            # Get preprocessing results from LLM
            response_raw = self.llm_client.chat(prompt,LLMProvider.TOOL_CALL)
            # Parse JSON response
            try:
                response_json = response_raw[response_raw.find('{'):response_raw.rfind('}')+1]
                preprocessing_result = json.loads(response_json)
                # Validate the preprocessing result
                if self._validate_preprocessing_result(preprocessing_result):
                    # Truncate metadata to prevent chunk size issues
                    if 'metadata' in preprocessing_result:
                        preprocessing_result['metadata'] = _truncate_metadata(preprocessing_result['metadata'])
                    logger.info(f"Document processed successfully, collection type: {preprocessing_result.get('collection_type')}")
                    return preprocessing_result
                else:
                    logger.warning("Invalid preprocessing result, using fallback")
                    return self._get_fallback_preprocessing(filename)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse LLM response as JSON: {response_raw}")
                return self._get_fallback_preprocessing(filename)
        except Exception as e:
            logger.error(f"Error in document preprocessing: {e}")
            return self._get_fallback_preprocessing(filename)

    def _validate_preprocessing_result(self, result: Dict[str, Any]) -> bool:
        """
        Validate the preprocessing result from LLM.

        Args:
            result: The preprocessing result to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = ["renamed_filename", "description", "abstract", "cleaned_content", "collection_type"]

        # Check if all required keys are present
        if not all(key in result for key in required_keys):
            logger.warning(f"Missing required keys in preprocessing result. Expected: {required_keys}, Got: {list(result.keys())}")
            return False

        # Check if collection_type is valid
        collection_type = result.get("collection_type")
        if collection_type not in COLLECTION_CONFIGS:
            logger.warning(f"Invalid collection type: {collection_type}")
            return False

        return True

    def _get_fallback_preprocessing(self, filename: str = "") -> Dict[str, Any]:
        """
        Get a fallback preprocessing result when LLM preprocessing fails.

        Args:
            filename: Optional filename for heuristic processing

        Returns:
            Fallback preprocessing result
        """
        from datetime import datetime

        # Simple heuristic based on filename
        filename_lower = filename.lower() if filename else ""

        if any(keyword in filename_lower for keyword in ["resume", "cv", "简历"]):
            collection_type = COLLECTION_RESUMES
            description = "个人简历文档"
            abstract = "包含个人信息、工作经验和技能的简历文档"
        elif any(keyword in filename_lower for keyword in ["project", "experience", "项目", "经验"]):
            collection_type = COLLECTION_PROJECTS_EXPERIENCE
            description = "项目经验文档"
            abstract = "描述项目经验和技术实现的文档"
        elif any(keyword in filename_lower for keyword in ["job", "jd", "posting", "招聘", "职位"]):
            collection_type = COLLECTION_JOB_POSTINGS
            description = "职位招聘信息"
            abstract = "包含职位要求和公司信息的招聘文档"
        else:
            collection_type = COLLECTION_PROJECTS_EXPERIENCE
            description = "通用文档"
            abstract = "未能自动分类的通用文档"

        fallback_filename = filename if filename and filename != "未知" else f"文档_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        return {
            "renamed_filename": fallback_filename,
            "description": description,
            "abstract": abstract,
            "cleaned_content": "原始内容（未清理）",  # This would need the original content
            "collection_type": collection_type,
            "metadata": _truncate_metadata({
                "source": "fallback_processing",
                "processing_method": "heuristic"
            }),
            "confidence": 0.3,  # Low confidence for fallback
            "reasoning": "基于文件名的启发式处理（LLM处理失败）"
        }

# Global document processor instance
_document_processor = None

def get_document_processor() -> DocumentProcessor:
    """Get or create singleton document processor."""
    global _document_processor
    if _document_processor is None:
        _document_processor = DocumentProcessor()
    return _document_processor
