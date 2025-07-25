import json
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from crewai.tools import BaseTool


class JSONParserInput(BaseModel):
    """向量搜索工具输入参数"""
    json_string: str = Field(
        description="The JSON string to be validated"
    )


class JSONParserTool(BaseTool):
    name: str = "json_parser_tool"
    description: str = "The tool is used when you want to validation the format of your final result json. It will provides detailed error information if your input is invalid"
    args_schema: type[BaseModel] = JSONParserInput

    def _run(self, json_string: str) -> str:
        try:
            parsed_data = json.loads(json_string)
            return json.dumps({
                "valid": True,
                "message": "JSON format is valid, you can use it as your final result response.",
                "data_type": type(parsed_data).__name__,
                "size": len(str(parsed_data))
            }, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return json.dumps({
                "valid": False,
                "error": str(e),
                "error_type": "JSONDecodeError",
                "line": getattr(e, 'lineno', None),
                "column": getattr(e, 'colno', None),
                "position": getattr(e, 'pos', None)
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "valid": False,
                "error": str(e),
                "error_type": type(e).__name__
            }, ensure_ascii=False)
