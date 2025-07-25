"""
Question Service - Tech Domain Generation
File: app/question_service/service.py
Purpose: Tech domain generation using LLM
"""

from app.agentic_core.llm_router.llm_client import get_llm_client_manager
from typing import List, Dict

from app.shared_kernel.exceptions import TechCoachException
from app.shared_kernel.database_service import TechDomainDBService

class TechDomainGenerator:
    """Service for generating dynamic tech domains based on user profile."""
    
    db_service = TechDomainDBService()

    def __init__(self):
        self.llm_client = get_llm_client_manager()
    
    def generate_tech_domains(self) -> List[Dict[str, str]]:
        """
        Generate tech domains based on user profile and existing domains
        
        Returns:
            List of dictionaries: [{"name": "", "description": ""}]
        """
        HARD_CODED_CONTEXT = "3年工作经验后端开发程序员，求职方向：高并发服务器，C++，Golang"

        # load from db
        current_domains = self.db_service.get_all_tech_domains()
        current_domains = [d.name for d in current_domains]
        
        existing_domains_str = ", ".join(current_domains) if current_domains else "无"
        prompt = f"""
我正在进行找工作的准备，首先，我先向你提供我的一些信息：{HARD_CODED_CONTEXT}

我希望你能够匹配我的信息中的个人背景、技术栈、项目经验和求职目标等信息，尽量全面地为我推荐在面试中需要重点准备的技术领域，具体要求如下：

- 应该考虑我的背景信息进行生成，假设我是后端开发，那么应该需要准备操作系统，计算机网络等。
- 当前我已经列出来的技术领域有这些：“{existing_domains_str}”，与这里面覆盖的或者有交集的技术领域，不用重复生成。
- 技术领域用中文，输出格式严格的JSON数组：[{{"name": "领域名称"}}]
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
                
                # Validate domains structure - 只检查name
                valid_domains = []
                for domain in domains:
                    if isinstance(domain, dict) and "name" in domain:
                        valid_domains.append({
                            "name": str(domain["name"]).strip()[:20]
                        })
                
                if valid_domains:
                    return valid_domains
        
        except Exception as e:
            # 捕获并处理异常
            raise TechCoachException(f"Failed to parse tech domains: {str(e)}")


# Global service instances
tech_domain_service = TechDomainGenerator()
# tech_question_service = TechDomainQuestionGenerator()