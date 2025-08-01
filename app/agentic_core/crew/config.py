"""
CrewAI 配置管理

定义 CrewAI 相关的配置类和默认设置。
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class AgentConfig:
    """Agent 配置类"""
    role: str
    goal: str
    backstory: str
    verbose: bool = True
    allow_delegation: bool = False
    max_iter: int = 5
    memory: bool = True
    tools: List[str] = field(default_factory=list)
    llm: str = "default"  # 使用默认 LLM 客户端


@dataclass
class TaskConfig:
    """Task 配置类"""
    name: str
    description: str
    expected_output: str
    agent_role: str
    tools: List[str] = field(default_factory=list)
    context: Optional[List[str]] = None
    output_file: Optional[str] = None


@dataclass
class CrewConfig:
    """Crew 配置类"""
    name: str
    description: str
    agents: List[str] = field(default_factory=list)
    tasks: List[str] = field(default_factory=list)
    verbose: bool = True
    memory: bool = True
    process: str = "hierarchical"  # sequential, hierarchical
    manager_llm: Optional[Dict[str, Any]] = None
    
    def add_agent(self, agent_config: AgentConfig):
        """添加 Agent 配置"""
        self.agents.append(agent_config)
    
    def add_task(self, task_config: TaskConfig):
        """添加 Task 配置"""
        self.tasks.append(task_config)
