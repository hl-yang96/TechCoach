"""
向量数据库查询工具

基于 ChromaDB 和 LlamaIndex 的向量数据库查询工具，专为 CrewAI Agents 设计。
支持多集合查询、结构化返回和灵活的参数配置。
"""

import logging, sys
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..rag.document_store import DocumentStore, get_document_store
from ..rag.config import get_all_collection_types, get_collection_config

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VectorSearchResult:
    """向量搜索结果结构"""
    source: str  # 来源文件
    text: str    # 文本chunk
    score: float # 相关性分数
    collection: str  # 所属集合
    metadata: Dict[str, Any]  # 元数据
    rank: int    # 排名


class VectorSearchInput(BaseModel):
    """向量搜索工具输入参数"""
    query: str = Field(
        description="查询文本，用于向量相似性搜索"
    )
    collections: Optional[List[str]] = Field(
        default=None,
        description="要搜索的集合列表。可选值: resumes, projects_experience, job_postings。如果为空则搜索所有可用集合"
        # description="要搜索的集合列表。可选值: resumes, projects_experience, job_postings, interviews, interview_qna_bank, code_analysis, industry_trends。如果为空则搜索所有可用集合"
    )
    top_k: int = Field(
        default=5,
        description="返回的最相关结果数量，默认为5"
    )
    min_score: float = Field(
        default=0.4,
        description="最小相关性分数阈值，低于此分数的结果将被过滤 (在当前数据质量下,一般情况最高相关性只达到0.6)，默认0.4"
    )


class VectorSearchTool(BaseTool):
    """
    向量数据库查询工具

    这个工具允许 CrewAI Agents 查询向量数据库中的相关文档。
    支持多个集合的查询，并返回结构化的搜索结果。
    """

    name: str = "vector_search"
    description: str = """
    向量数据库查询工具，用于在文档集合中搜索与查询相关的内容。

    支持的集合类型：
    - resumes: 个人简历
    - projects_experience: 项目和工作经验
    - job_postings: 职位招聘信息
    
    返回结构化的搜索结果，包含来源文件、文本内容、相关性分数等信息。

    注意: 在调用工具生成结构化参数的时候，外层不要加方括号
    """
    args_schema: type[BaseModel] = VectorSearchInput

    # Use model_config to allow arbitrary types and exclude document_store from validation
    model_config = {"arbitrary_types_allowed": True}
    
    def __init__(self, **kwargs):
        """
        初始化向量搜索工具

        Args:
            document_store: DocumentStore 实例，如果为 None 则创建新实例
        """
        super().__init__(**kwargs)
        # Store document_store as instance attribute, not part of Pydantic model
        self._document_store = get_document_store()

    @property
    def document_store(self) -> DocumentStore:
        """Get the document store instance."""
        return self._document_store
        
    def _run(
        self,
        query: str,
        collections: Optional[List[str]] = None,
        top_k: int = 5,
        min_score: float = 0.4
    ) -> str:
        try:
            if collections:
                available_collections = get_all_collection_types()
                invalid_collections = [c for c in collections if c not in available_collections]
                if invalid_collections:
                    return f"错误：无效的集合类型: {invalid_collections}。可用集合: {available_collections}"
            
            # 执行搜索
            search_results = self.document_store.search_documents(
                query_text=query,
                collection_types=collections,
                top_k=top_k
            )
            
            if not search_results:
                return f"未找到与查询 '{query}' 相关的结果"
            
            # 过滤低分结果
            filtered_results = [
                result for result in search_results 
                if result.get('score', 0.0) >= min_score
            ]
            
            if not filtered_results:
                return f"未找到相关性分数高于 {min_score} 的结果"
            
            # 转换为结构化结果
            structured_results = []
            for i, result in enumerate(filtered_results):
                structured_result = VectorSearchResult(
                    source=result.get('source', 'unknown'),
                    text=result.get('content', ''),
                    score=result.get('score', 0.0),
                    collection=result.get('collection_type', 'unknown'),
                    metadata=result.get('metadata', {}),
                    rank=i + 1
                )
                structured_results.append(structured_result)
            
            # 格式化输出
            return self._format_results(structured_results, query)
            
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            return f"搜索失败: {str(e)}"
    
    def _format_results(self, results: List[VectorSearchResult], query: str) -> str:
        if not results:
            return f"预处理完成，未找到与查询 '{query}' 相关的结果"
        
        output_lines = [
            f"=== 向量搜索结果 (查询: '{query}') ===",
            f"找到 {len(results)} 个相关结果:\n"
        ]
        
        for result in results:
            collection_config = get_collection_config(result.collection)
            collection_desc = collection_config.get('description', result.collection)
            result_block = [
                f"【排名 {result.rank}】",
                f"来源: {result.source}",
                f"集合: {result.collection} ({collection_desc})",
                f"相关性: {result.score:.3f}",
                f"内容: {result.text}",
            ]
            
            # 添加关键元数据
            if result.metadata:
                key_metadata = {}
                # 选择最重要的元数据字段显示
                important_fields = ['target_job', 'company_name', 'job_title', 'project_name', 
                                  'document_type', 'interview_date', 'source', 'key_topics']
                for field in important_fields:
                    if field in result.metadata:
                        key_metadata[field] = result.metadata[field]
                
                if key_metadata:
                    metadata_str = ", ".join([f"{k}: {v}" for k, v in key_metadata.items()])
                    result_block.append(f"元数据: {metadata_str}")
            
            output_lines.append("\n".join(result_block))
            output_lines.append("-" * 50)
        
        # 添加搜索统计
        collections_searched = list(set(result.collection for result in results))
        output_lines.append(f"\n搜索的集合: {', '.join(collections_searched)}")
        output_lines.append(f"平均相关性: {sum(r.score for r in results) / len(results):.3f}")
        
        return "\n".join(output_lines)
    
    def get_available_collections(self) -> List[str]:
        """获取可用的集合列表"""
        return get_all_collection_types()
    
    def get_collection_info(self, collection_type: str) -> Dict[str, Any]:
        """获取集合信息"""
        return get_collection_config(collection_type)
