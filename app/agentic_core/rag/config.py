"""
RAG Configuration Constants
File: app/agentic_core/rag/config.py
Purpose: Global configuration constants for RAG system based on user stories
"""

from typing import Dict, Any, List
from enum import Enum


# ============================================================================
# EMBEDDING AND VECTOR CONFIGURATION
# ============================================================================

# Embedding model configuration
EMBEDDING_MODEL_NAME = "text-embedding-004"
EMBEDDING_BATCH_SIZE = 100
EMBEDDING_DIMENSION = 768  # Google Gemini text-embedding-004 dimension

# Metadata length limits to avoid chunk size issues
MAX_METADATA_FIELD_LENGTH = 50  # Maximum characters for any single metadata field
MAX_SUMMARY_LENGTH = 100  # Maximum length for document summary
MAX_KEYWORDS_COUNT = 5  # Maximum number of keywords

# Global chunk size configurations for different document types
CHUNK_SIZE_RESUMES = 256  # Smaller chunks for precise resume matching
CHUNK_SIZE_PROJECTS = 512  # Medium chunks for project descriptions
CHUNK_SIZE_JOB_POSTINGS = 384  # Medium-small chunks for job requirements
CHUNK_SIZE_INTERVIEWS = 256  # Small chunks for interview Q&A
CHUNK_SIZE_QNA_BANK = 128  # Very small chunks for specific questions
CHUNK_SIZE_CODE_ANALYSIS = 1024  # Large chunks for code context
CHUNK_SIZE_INDUSTRY_TRENDS = 512  # Medium chunks for trend analysis

# Chunk overlap configurations
CHUNK_OVERLAP_RESUMES = 20
CHUNK_OVERLAP_PROJECTS = 50
CHUNK_OVERLAP_JOB_POSTINGS = 30
CHUNK_OVERLAP_INTERVIEWS = 20
CHUNK_OVERLAP_QNA_BANK = 10
CHUNK_OVERLAP_CODE_ANALYSIS = 100
CHUNK_OVERLAP_INDUSTRY_TRENDS = 50

# Retrieval configurations
SIMILARITY_TOP_K_DEFAULT = 10
SIMILARITY_TOP_K_RESUMES = 5
SIMILARITY_TOP_K_PROJECTS = 8
SIMILARITY_TOP_K_JOB_POSTINGS = 6
SIMILARITY_TOP_K_INTERVIEWS = 12
SIMILARITY_TOP_K_QNA_BANK = 15
SIMILARITY_TOP_K_CODE_ANALYSIS = 5
SIMILARITY_TOP_K_INDUSTRY_TRENDS = 8


# ============================================================================
# COLLECTION DEFINITIONS (Based on User Stories)
# ============================================================================

class CollectionType(str, Enum):
    """Collection types based on user stories."""
    # Phase 1: Core Job-Seeking Profile
    RESUMES = "resumes"
    PROJECTS_EXPERIENCE = "projects_experience"
    JOB_POSTINGS = "job_postings"
    
    # Phase 2: Deepening Insights & Market Alignment
    INTERVIEWS = "interviews"
    INTERVIEW_QNA_BANK = "interview_qna_bank"
    CODE_ANALYSIS = "code_analysis"
    INDUSTRY_TRENDS = "industry_trends"


# Collection configurations based on user stories
COLLECTION_CONFIGS: Dict[str, Dict[str, Any]] = {
    # Phase 1 Collections
    CollectionType.RESUMES: {
        "name": "resumes",
        "description": "存储用户所有版本的个人简历。用于快速查找、匹配和定制简历以适应不同岗位。",
        "metadata": {
            "type": "resume",
            "purpose": "job_matching",
            "phase": 1
        },
        "chunk_size": CHUNK_SIZE_RESUMES,
        "chunk_overlap": CHUNK_OVERLAP_RESUMES,
        "similarity_top_k": SIMILARITY_TOP_K_RESUMES,
        "required_metadata_fields": ["target_job", "language", "last_updated"],
        "optional_metadata_fields": ["version", "company_focus"]
    },
    
    CollectionType.PROJECTS_EXPERIENCE: {
        "name": "projects_experience",
        "description": "存储用户所有项目和工作经验的详细材料，作为简历内容的支撑和扩展。",
        "metadata": {
            "type": "experience",
            "purpose": "resume_support",
            "phase": 1
        },
        "chunk_size": CHUNK_SIZE_PROJECTS,
        "chunk_overlap": CHUNK_OVERLAP_PROJECTS,
        "similarity_top_k": SIMILARITY_TOP_K_PROJECTS,
        "required_metadata_fields": ["project_name", "document_type", "is_technical"],
        "optional_metadata_fields": ["related_resume_version", "tech_stack", "duration"]
    },
    
    CollectionType.JOB_POSTINGS: {
        "name": "job_postings",
        "description": "存储收集到的目标岗位JD。用于市场需求分析、技能差距识别和简历匹配。",
        "metadata": {
            "type": "job_posting",
            "purpose": "market_analysis",
            "phase": 1
        },
        "chunk_size": CHUNK_SIZE_JOB_POSTINGS,
        "chunk_overlap": CHUNK_OVERLAP_JOB_POSTINGS,
        "similarity_top_k": SIMILARITY_TOP_K_JOB_POSTINGS,
        "required_metadata_fields": ["company_name", "job_title", "source_url"],
        "optional_metadata_fields": ["salary_range", "location", "experience_level"]
    },
    
    # Phase 2 Collections
    CollectionType.INTERVIEWS: {
        "name": "interviews",
        "description": "存储所有面试的记录、问题和反馈。用于复盘、发现知识盲区和预测高频考点。",
        "metadata": {
            "type": "interview",
            "purpose": "interview_prep",
            "phase": 2
        },
        "chunk_size": CHUNK_SIZE_INTERVIEWS,
        "chunk_overlap": CHUNK_OVERLAP_INTERVIEWS,
        "similarity_top_k": SIMILARITY_TOP_K_INTERVIEWS,
        "required_metadata_fields": ["company_name", "job_title", "interview_round", "result", "interview_date"],
        "optional_metadata_fields": ["interviewer", "difficulty", "feedback"]
    },
    
    CollectionType.INTERVIEW_QNA_BANK: {
        "name": "interview_qna_bank",
        "description": "从互联网、论坛、GitHub等渠道收集的通用面试题库，用于补充和扩展个人面试经验，进行模拟训练。",
        "metadata": {
            "type": "qna_bank",
            "purpose": "interview_training",
            "phase": 2
        },
        "chunk_size": CHUNK_SIZE_QNA_BANK,
        "chunk_overlap": CHUNK_OVERLAP_QNA_BANK,
        "similarity_top_k": SIMILARITY_TOP_K_QNA_BANK,
        "required_metadata_fields": ["source", "job_domain", "question_type"],
        "optional_metadata_fields": ["difficulty", "frequency", "tags"]
    },
    
    CollectionType.CODE_ANALYSIS: {
        "name": "code_analysis",
        "description": "（针对开发者）存储对用户代码库的静态分析结果和摘要。用于客观评估技术能力和梳理技术亮点。",
        "metadata": {
            "type": "code_analysis",
            "purpose": "skill_assessment",
            "phase": 2
        },
        "chunk_size": CHUNK_SIZE_CODE_ANALYSIS,
        "chunk_overlap": CHUNK_OVERLAP_CODE_ANALYSIS,
        "similarity_top_k": SIMILARITY_TOP_K_CODE_ANALYSIS,
        "required_metadata_fields": ["repo_name", "primary_language", "key_frameworks", "analysis_date"],
        "optional_metadata_fields": ["complexity_score", "test_coverage", "code_quality"]
    },
    
    CollectionType.INDUSTRY_TRENDS: {
        "name": "industry_trends",
        "description": "存储行业报告和技术趋势分析文章。用于提升对话的战略高度和行业视野。",
        "metadata": {
            "type": "industry_trends",
            "purpose": "market_insight",
            "phase": 2
        },
        "chunk_size": CHUNK_SIZE_INDUSTRY_TRENDS,
        "chunk_overlap": CHUNK_OVERLAP_INDUSTRY_TRENDS,
        "similarity_top_k": SIMILARITY_TOP_K_INDUSTRY_TRENDS,
        "required_metadata_fields": ["report_source", "publish_date", "key_topics"],
        "optional_metadata_fields": ["industry", "region", "trend_type"]
    }
}


# ============================================================================
# LLM CLASSIFICATION PROMPTS
# ============================================================================

DOCUMENT_CLASSIFICATION_PROMPT = """
你是一个专业的文档分类专家。请分析以下文档内容，并确定它应该属于哪个集合(collection)以及相应的元数据。

可选的集合类型：
1. resumes - 个人简历
2. projects_experience - 项目和工作经验
3. job_postings - 职位招聘信息
4. interviews - 面试记录
5. interview_qna_bank - 面试题库
6. code_analysis - 代码分析报告
7. industry_trends - 行业趋势报告

文档内容：
{document_content}

文档文件名：{filename}

请以JSON格式返回分类结果，包含：
1. collection_type: 集合类型
2. metadata: 相关元数据字典(每个字段限制30字符以内,简单K-V,V只能是字符串或者数字)
3. confidence: 分类置信度 (0-1)
4. reasoning: 分类理由(限制50字符以内)

示例输出：
{{
    "collection_type": "resumes",
    "metadata": {{
        "target_job": "软件工程师",
        "language": "中文",
        "last_updated": "2025-07-20"
    }},
    "confidence": 0.95,
    "reasoning": "简历内容"
}}
不要输出处理json外的任何其他的文字或者格式符号等。
"""

METADATA_ENHANCEMENT_PROMPT = """
你是一个元数据增强专家。请为以下文档生成丰富的元数据，以便更好地进行检索和分析。

集合类型：{collection_type}
文档内容：{document_content}
当前元数据：{current_metadata}

必需的元数据字段：{required_fields}
可选的元数据字段：{optional_fields}

请以JSON格式返回增强后的元数据：
{{
    "enhanced_metadata": {{
        // 增强后的完整元数据(简单K-V,V只能是字符串或者数字;每个字段限制50字符以内)
    }},
    "extracted_keywords": [
        // 从文档中提取的关键词(最多5个,每个限制20字符)
    ],
    "summary": "文档内容摘要(限制100字符以内)"
}}
不要输出处理json外的任何其他的文字或者格式符号等。
"""


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_collection_config(collection_type: str) -> Dict[str, Any]:
    """Get configuration for a specific collection type."""
    return COLLECTION_CONFIGS.get(collection_type, {})


def get_chunk_config(collection_type: str) -> Dict[str, int]:
    """Get chunk configuration for a specific collection type."""
    config = get_collection_config(collection_type)
    return {
        "chunk_size": config.get("chunk_size", 512),
        "chunk_overlap": config.get("chunk_overlap", 50)
    }


def get_retrieval_config(collection_type: str) -> Dict[str, int]:
    """Get retrieval configuration for a specific collection type."""
    config = get_collection_config(collection_type)
    return {
        "similarity_top_k": config.get("similarity_top_k", SIMILARITY_TOP_K_DEFAULT)
    }


def get_all_collection_types() -> List[str]:
    """Get all available collection types."""
    return list(COLLECTION_CONFIGS.keys())
