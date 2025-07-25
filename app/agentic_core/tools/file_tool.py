import os
import json
from pathlib import Path
from pydantic import BaseModel,Field
from typing import List, Optional
from crewai.tools import BaseTool


class GetExistFileListTool(BaseTool):
    name: str = "get_exist_file_list_tool"
    description: str = "Lists all the documents locally. Then you can use another tool \"read_file_tool\" to read the content of the file you want."

    def _run(self) -> str:
        try:
            documents_dir = Path("app_data/documents")
            if not documents_dir.exists():
                return json.dumps({
                    "success": False,
                    "error": "Documents directory does not exist",
                    "files": []
                }, ensure_ascii=False)

            files = []
            for file_path in documents_dir.iterdir():
                if file_path.is_file():
                    files.append({
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime
                    })

            return json.dumps({
                "success": True,
                "count": len(files),
                "files": files
            }, ensure_ascii=False)

        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e),
                "files": []
            }, ensure_ascii=False)


class ReadFileToolInput(BaseModel):
    filename: str = Field(
        description="The name of the file to read from the documents directory. It should be a file name without path."
    )
    max_tokens: int = Field(
        default=10000,
        description="Maximum number of tokens to read from the file. If the content exceeds this limit, it will be truncated."
    )

class ReadFileTool(BaseTool):
    name: str = "read_file_tool"
    description: str = "Reads content from the file specified by filename. Before calling the tool, you should get all the existed file by another tool. If the content exceeds max_tokens, it will be truncated."
    args_schema: type[BaseModel] = ReadFileToolInput

    def _run(self, filename: str, max_tokens: int = 10000) -> str:
        try:
            documents_dir = Path("app_data/documents")
            if not filename.startswith("app_data/documents"):
                file_path = documents_dir / filename
            else:
                file_path = Path(filename)

            if not file_path.exists():
                return json.dumps({
                    "success": False,
                    "error": f"File '{filename}' does not exist",
                    "content": ""
                }, ensure_ascii=False)

            if not file_path.is_file():
                return json.dumps({
                    "success": False,
                    "error": f"'{filename}' is not a file",
                    "content": ""
                }, ensure_ascii=False)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if len(content) > max_tokens:
                content = content[:max_tokens]
                truncated = True
            else:
                truncated = False

            return json.dumps({
                "success": True,
                "filename": filename,
                "content": content,
                "truncated": truncated,
                "content_length": len(content),
                "file_size": file_path.stat().st_size
            }, ensure_ascii=False)

        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e),
                "content": ""
            }, ensure_ascii=False)
