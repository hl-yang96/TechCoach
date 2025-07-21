"""
Document Classifier for TechCoach RAG System
File: app/agentic_core/rag/document_classifier.py
Purpose: LLM-based document classification and metadata generation
"""

import json
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from ..llm_router.llm_client import get_llm_client
from .config import (
    DOCUMENT_CLASSIFICATION_PROMPT,
    METADATA_ENHANCEMENT_PROMPT,
    COLLECTION_CONFIGS,
    CollectionType
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


class DocumentClassifier:
    """
    LLM-based document classifier for automatic collection assignment and metadata generation.
    
    This class uses the LLM router to:
    1. Classify documents into appropriate collections
    2. Generate relevant metadata based on document content
    3. Enhance existing metadata with additional insights
    """
    
    def __init__(self):
        """Initialize the document classifier."""
        self.llm_client = get_llm_client()
        
    def classify_document(self, document_content: str, filename: str = "") -> Dict[str, Any]:
        """
        Classify a document and determine its collection type and metadata.
        
        Args:
            document_content: The content of the document to classify
            filename: Optional filename for additional context
            
        Returns:
            Dictionary containing classification results
        """
        try:
            # Prepare the prompt
            prompt = DOCUMENT_CLASSIFICATION_PROMPT.format(
                document_content=document_content[:2000],  # Limit content length
                filename=filename
            )
            
            # Get classification from LLM
            response = self.llm_client.chat(prompt)
            
            # Parse JSON response
            try:
                # regex to match from first '{' to last '}'
                response = response[response.find('{'):response.rfind('}')+1]

                classification_result = json.loads(response)
                
                # Validate the result
                if self._validate_classification_result(classification_result):
                    # Truncate metadata to prevent chunk size issues
                    if 'metadata' in classification_result:
                        classification_result['metadata'] = _truncate_metadata(classification_result['metadata'])

                    logger.info(f"Document classified as: {classification_result.get('collection_type')}")
                    return classification_result
                else:
                    logger.warning("Invalid classification result, using fallback")
                    return self._get_fallback_classification(filename)
                    
            except json.JSONDecodeError:
                logger.error(f"Failed to parse LLM response as JSON: {response}")
                return self._get_fallback_classification(filename)
                
        except Exception as e:
            logger.error(f"Error in document classification: {e}")
            return self._get_fallback_classification(filename)
    
    def enhance_metadata(self, 
                        collection_type: str, 
                        document_content: str, 
                        current_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance existing metadata with additional insights from LLM.
        
        Args:
            collection_type: The collection type for the document
            document_content: The content of the document
            current_metadata: Current metadata to enhance
            
        Returns:
            Enhanced metadata dictionary
        """
        try:
            # Get collection configuration
            config = COLLECTION_CONFIGS.get(collection_type, {})
            required_fields = config.get("required_metadata_fields", [])
            optional_fields = config.get("optional_metadata_fields", [])
            
            # Prepare the prompt
            prompt = METADATA_ENHANCEMENT_PROMPT.format(
                collection_type=collection_type,
                document_content=document_content[:2000],  # Limit content length
                current_metadata=json.dumps(current_metadata, ensure_ascii=False),
                required_fields=required_fields,
                optional_fields=optional_fields
            )
            
            # Get enhancement from LLM
            response = self.llm_client.chat(prompt)
            
            # Parse JSON response
            try:
                response = response[response.find('{'):response.rfind('}')+1]
                enhancement_result = json.loads(response)
                enhanced_metadata = enhancement_result.get("enhanced_metadata", current_metadata)
                
                # Merge with current metadata
                final_metadata = {**current_metadata, **enhanced_metadata}
                
                # Truncate metadata to prevent chunk size issues
                final_metadata = _truncate_metadata(final_metadata)

                logger.info(f"Enhanced metadata for {collection_type}: {final_metadata}")
                return final_metadata
                
            except json.JSONDecodeError:
                logger.error(f"Failed to parse metadata enhancement response: {response}")
                return current_metadata
                
        except Exception as e:
            logger.error(f"Error in metadata enhancement: {e}")
            return current_metadata
    
    def get_collection_and_metadata(self,
                                  document_content: str,
                                  filename: str = "") -> Tuple[str, Dict[str, Any], str]:
        """
        Get both collection type, enhanced metadata, and generated filename for a document.

        Args:
            document_content: The content of the document
            filename: Optional filename for additional context

        Returns:
            Tuple of (collection_type, metadata, final_filename)
        """
        # First classify the document
        classification = self.classify_document(document_content, filename or "未知")
        collection_type = classification.get("collection_type", CollectionType.PROJECTS_EXPERIENCE)
        base_metadata = classification.get("metadata", {})

        # Handle generated filename
        final_filename = filename
        if not filename or filename == "未知":
            generated_filename = classification.get("generated_filename")
            if generated_filename:
                final_filename = generated_filename
            else:
                # Fallback to timestamp-based filename
                from datetime import datetime
                final_filename = f"文档_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Add classification confidence and reasoning
        base_metadata["classification_confidence"] = classification.get("confidence", 0.5)
        base_metadata["classification_reasoning"] = classification.get("reasoning", "")
        base_metadata["final_filename"] = final_filename

        # Enhance the metadata
        enhanced_metadata = self.enhance_metadata(collection_type, document_content, base_metadata)

        # TODO: the auto-generated tag sometime is too many, need to deal with it

        return collection_type, enhanced_metadata, final_filename
    
    def _validate_classification_result(self, result: Dict[str, Any]) -> bool:
        """
        Validate the classification result from LLM.
        
        Args:
            result: The classification result to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["collection_type", "metadata", "confidence"]
        
        # Check if all required keys are present
        if not all(key in result for key in required_keys):
            return False
        
        # Check if collection_type is valid
        collection_type = result.get("collection_type")
        if collection_type not in COLLECTION_CONFIGS:
            return False
        
        # Check if confidence is a valid number
        confidence = result.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            return False
        
        # Check if metadata is a dictionary
        metadata = result.get("metadata")
        if not isinstance(metadata, dict):
            return False
        
        return True
    
    def _get_fallback_classification(self, filename: str = "") -> Dict[str, Any]:
        """
        Get a fallback classification when LLM classification fails.
        
        Args:
            filename: Optional filename for heuristic classification
            
        Returns:
            Fallback classification result
        """
        # Simple heuristic based on filename
        filename_lower = filename.lower()
        
        if any(keyword in filename_lower for keyword in ["resume", "cv", "简历"]):
            collection_type = CollectionType.RESUMES
            metadata = {
                "target_job": "未知",
                "language": "中文" if any(char in filename for char in "中文简历") else "英文",
                "last_updated": "2025-07-20"
            }
        elif any(keyword in filename_lower for keyword in ["project", "experience", "项目", "经验"]):
            collection_type = CollectionType.PROJECTS_EXPERIENCE
            metadata = {
                "project_name": filename,
                "document_type": "项目描述",
                "is_technical": True
            }
        elif any(keyword in filename_lower for keyword in ["job", "jd", "posting", "招聘", "职位"]):
            collection_type = CollectionType.JOB_POSTINGS
            metadata = {
                "company_name": "未知公司",
                "job_title": "未知职位",
                "source_url": ""
            }
        else:
            # Default to projects_experience
            collection_type = CollectionType.PROJECTS_EXPERIENCE
            metadata = {
                "project_name": filename or "未知文档",
                "document_type": "其他",
                "is_technical": False
            }
        
        # Truncate metadata to prevent chunk size issues
        metadata = _truncate_metadata(metadata)

        return {
            "collection_type": collection_type,
            "metadata": metadata,
            "confidence": 0.3,  # Low confidence for fallback
            "reasoning": "基于文件名的启发式分类（LLM分类失败）"
        }


# Global document classifier instance
_document_classifier = None

def get_document_classifier() -> DocumentClassifier:
    """Get or create singleton document classifier."""
    global _document_classifier
    if _document_classifier is None:
        _document_classifier = DocumentClassifier()
    return _document_classifier
