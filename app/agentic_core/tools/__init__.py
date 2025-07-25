"""
AI Tools Package
File: app/agentic_core/tools/__init__.py
Created: 2025-07-17
Purpose: Custom AI tools and integrations for agentic workflows
"""

from .vector_search_tool import VectorSearchTool
from .file_tool import ReadFileTool, GetExistFileListTool
from .json_parser_tool import JSONParserTool

TOOL_GET_EXIST_FILE_LIST = "get_exist_file_list"
TOOL_READ_FILE           = "read_file_tool"
TOOL_VECTOR_SEARCH       = "vector_search"
TOOL_JSON_PARSER         = "json_parser"

AllTools = [
    TOOL_GET_EXIST_FILE_LIST,
    TOOL_READ_FILE,
    TOOL_VECTOR_SEARCH,
    TOOL_JSON_PARSER
]

def create_all_tools() -> dict:
    """Create and return all available tools."""
    return {
        TOOL_GET_EXIST_FILE_LIST: GetExistFileListTool(),
        TOOL_READ_FILE: ReadFileTool(),
        TOOL_VECTOR_SEARCH: VectorSearchTool(),
        TOOL_JSON_PARSER: JSONParserTool()
    }

__all__ = [
    'VectorSearchTool'
]