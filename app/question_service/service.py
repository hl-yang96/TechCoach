"""
Question Service - Tech Domain Generation
File: app/question_service/service.py
Purpose: Tech domain generation using LLM
"""

from app.agentic_core.llm_router.llm_client import get_llm_client
from typing import List, Dict


class TechDomainGenerator:
    """Service for generating dynamic tech domains based on user profile."""
    
    def __init__(self):
        self.llm_client = get_llm_client()
    
    def generate_tech_domains(
        self, 
        current_domains: List[str] = None, 
        context: str = "3年工作经验后端开发程序员，求职方向：高并发服务器，C++，Golang"
    ) -> List[Dict[str, str]]:
        """
        Generate tech domains based on user profile and existing domains
        
        Args:
            current_domains: List of existing tech domains
            context: User's background context
            
        Returns:
            List of dictionaries: [{"name": "", "description": ""}]
        """
        current_domains = current_domains or []
        existing_domains_str = ", ".join(current_domains) if current_domains else "无"
        
        prompt = f"""
我正在进行找工作的准备，首先，我先向你提供我的一些信息：{context}

我希望你能够匹配我的信息中的个人背景、技术栈、项目经验和求职目标等信息，尽量全面地为我推荐在面试中需要重点准备的技术领域，具体要求如下：
- 假如我是后端开发，那么应该需要准备操作系统，计算机网络等
- 当前我已经列出来的技术领域有这些：“ {existing_domains_str}”，避免重复生成。
- 应该考虑我的背景信息进行生成。
- 输出格式严格的JSON数组：[{{"name": "领域名称", "description": "简短描述"}}]      
- 请用中文回答，示例：  [{{"name": "操作系统", "description": "现代操作系统相关基础和进阶知识"}}, {{"name": "C/C++", "description": "C/C++ 编程语言"}}]
        """
        
        response = self.llm_client.chat(prompt)
        return self._parse_tech_domains(response)
    
    def _parse_tech_domains(self, llm_response: str) -> List[Dict[str, str]]:
        """Parse LLM response to extract JSON array of domains."""
        import json
        import re
        
        try:
            # Try to find and extract JSON array from response
            json_pattern = r'\[(\s*{.*?}\s*)*\s*\]'
            json_match = re.search(json_pattern, llm_response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                domains = json.loads(json_str)
                
                # Validate domains structure
                valid_domains = []
                for domain in domains:
                    if isinstance(domain, dict) and "name" in domain and "description" in domain:
                        valid_domains.append({
                            "name": str(domain["name"]).strip()[:20],
                            "description": str(domain["description"]).strip()[:50]
                        })
                
                if valid_domains:
                    return valid_domains
        
        except Exception:
            pass
        
        # Fallback sample domains for C++/Golang backend developer
        sample_domains = [
            {"name": "高并发编程", "description": "并发控制与线程安全"},
            {"name": "网络编程", "description": "Socket通信与协议"},
            {"name": "服务器架构", "description": "微服务系统设计"},
            {"name": "数据库优化", "description": "索引与查询调优"},
            {"name": "缓存系统", "description": "Redis消息队列"},
            {"name": "DevOps工具链", "description": "Docker CI/CD"}
        ]
        
        return sample_domains


# Global service instance
tech_domain_service = TechDomainGenerator()