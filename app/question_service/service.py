"""
Question Service - Tech Domain Generation
File: app/question_service/service.py
Purpose: Tech domain generation using LLM
"""

from app.agentic_core.llm_router.llm_client import get_llm_client
from typing import List, Dict

from app.shared_kernel.exceptions import TechCoachException
from app.shared_kernel.database_service import TechDomainDBService

class TechDomainGenerator:
    """Service for generating dynamic tech domains based on user profile."""
    
    db_service = TechDomainDBService()

    def __init__(self):
        self.llm_client = get_llm_client()
    
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




################################## TechDomainQuestions ####################

class TechDomainQuestionGenerator:
    """Service for generating interview questions for tech domains using LLM"""

    def __init__(self):
        self.llm_client = get_llm_client()

    def generate_questions(self, domain_name: str, context: str = None) -> List[Dict[str, str]]:
        """
        Generate interview questions for a specific tech domain

        Args:
            domain_name: The tech domain to generate questions for
            context: User context (will be from RAG in the future)

        Returns:
            List of dictionaries: [{"question_text": "问题内容", "generated_answer": None}]
            注意：当前版本只生成问题，不生成参考答案
        """
        # TODO: 后续从 RAG 获取 context，现在使用硬编码
        HARD_CODED_CONTEXT = "4年工作经验后端开发程序员；求职方向：高并发服务器，C++，Golang; 项目经验：高并发内存索引服务，高并发广告服务器缓存服务，图数据库系统搭建"

        if context is None:
            context = HARD_CODED_CONTEXT

        prompt = f"""
我是一位求职者，我的背景信息：{context}

我现在需要你作为一个这个领域的面试辅导专家，为我生成"{domain_name}"这个技术领域的面试题库，要求如下：

1. 题目应该尽可能全面，我会按照这个题库，进行{domain_name}领域的复习，如果你生成的不够全面则会影响我的复习结果；
2. 题目和难度应该符合我的背景、经验水平、以及求职方向等信息，如果你出了太多不相关的问题，会对我的复习效率产生影响；
3. 如果能够与我的项目背景相结合进行出题就更好，但是不要臆断我的项目中可能的一些问题，你的问题必须是看起来靠谱的。

输出格式要求：严格按照以下 JSON List 格式输出，不要包含任何其他文字：

[
  "具体的面试题目1", "具体的面试题目2"
]
"""

        try:
            response = self.llm_client.chat(prompt)
            return self._parse_questions(response)
        except Exception as e:
            raise TechCoachException(f"Failed to generate questions for domain '{domain_name}': {str(e)}")

    def _parse_questions(self, llm_response: str) -> List[Dict[str, str]]:
        """Parse LLM response to extract JSON array of question strings."""
        import json
        import re

        try:
            # Try to find and extract JSON array from response
            json_pattern = r'\[(\s*".*?"\s*,?\s*)*\s*\]'
            json_match = re.search(json_pattern, llm_response, re.DOTALL)

            if json_match:
                json_str = json_match.group(0)
                questions_list = json.loads(json_str)

                # Convert string list to dict format for compatibility
                valid_questions = []
                for question_text in questions_list:
                    if isinstance(question_text, str) and question_text.strip():
                        valid_questions.append({
                            "question_text": str(question_text).strip(),
                            "generated_answer": None  # 不再生成参考答案
                        })

                if valid_questions:
                    return valid_questions

            # If parsing fails, return fallback questions
            raise ValueError("Failed to parse LLM response")

        except Exception as e:
            # 如果解析失败，返回备用问题
            raise TechCoachException(f"Failed to parse questions: {str(e)}")


# Global service instances
tech_domain_service = TechDomainGenerator()
tech_question_service = TechDomainQuestionGenerator()