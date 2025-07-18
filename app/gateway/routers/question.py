"""
Interview Question Management Router
File: app/gateway/routers/question.py
Created: 2025-07-17
Purpose: question generation and management
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.question_service.service import tech_domain_service

router = APIRouter()

class TechDomainRequest(BaseModel):
    current_domains: List[str] = []  # user's existing tech domains
    context: str = "3年工作经验后端开发程序员，求职方向：高并发服务器，C++，Golang"

class TechDomainResponse(BaseModel):
    domains: List[dict]  # [{"name": "", "description": ""}]

@router.post("/tech-domains/generate", response_model=TechDomainResponse)
async def generate_tech_domains(request: TechDomainRequest):
    """
    Generate dynamic tech domains based on user's profile and context
    """
    try:
        domains = tech_domain_service.generate_tech_domains(
            current_domains=request.current_domains,
            context=request.context
        )
        
        return TechDomainResponse(domains=domains)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate tech domains: {str(e)}")

@router.get("/tech-domains/sample")
async def get_sample_domains():
    """
    Return sample tech domains for testing without LLM call
    """
    return {
        "domains": [
            {"name": "高并发编程", "description": "分布式系统下的并发控制与优化"},
            {"name": "C++性能优化", "description": "C++代码性能分析和优化技术"},
            {"name": "Golang协程", "description": "Go语言goroutine和channel的使用"},
            {"name": "Redis高可用", "description": "Redis集群和缓存架构设计"},
            {"name": "MySQL优化", "description": "数据库索引优化和查询调优"}
        ]
    }

def parse_tech_domains(llm_response: str) -> List[dict]:
    """
    Parse LLM response to extract tech domains
    For now, using manual extraction - can be improved with better JSON parsing
    """
    # Fallback sample domains
    sample_domains = [
        {"name": "高并发编程", "description": "分布式系统下的并发控制与优化"},
        {"name": "网络编程", "description": "TCP/IP协议和socket编程实践"},
        {"name": "数据库优化", "description": "SQL优化和数据库架构设计"},
        {"name": "系统架构", "description": "微服务架构和系统重构"},
        {"name": "分布式系统", "description": "包括分布式锁、消息队列等"}
    ]
    
    # Try to extract JSON if present in response
    try:
        import json
        if "[" in llm_response and "]" in llm_response:
            json_start = llm_response.find("[")
            json_end = llm_response.rfind("]") + 1
            json_str = llm_response[json_start:json_end]
            return json.loads(json_str)
    except:
        pass
    
    return sample_domains

