"""
CrewAI 配置管理

定义 CrewAI 相关的配置类和默认设置。
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class AgentRole(Enum):
    """预定义的 Agent 角色"""
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    REVIEWER = "reviewer"
    COORDINATOR = "coordinator"


class TaskType(Enum):
    """任务类型枚举"""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"
    REVIEW = "review"
    COORDINATION = "coordination"


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
    llm_config: Optional[Dict[str, Any]] = None


@dataclass
class TaskConfig:
    """Task 配置类"""
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
    agents: List[AgentConfig] = field(default_factory=list)
    tasks: List[TaskConfig] = field(default_factory=list)
    verbose: bool = True
    memory: bool = True
    process: str = "sequential"  # sequential, hierarchical
    manager_llm: Optional[Dict[str, Any]] = None
    
    def add_agent(self, agent_config: AgentConfig):
        """添加 Agent 配置"""
        self.agents.append(agent_config)
    
    def add_task(self, task_config: TaskConfig):
        """添加 Task 配置"""
        self.tasks.append(task_config)


# 默认 Agent 配置模板 (已废弃 - 请使用 agent_manager.py 中的 PROFESSIONAL_AGENT_CONFIGS)
# @deprecated: 使用 PROFESSIONAL_AGENT_CONFIGS 替代
DEFAULT_AGENT_CONFIGS = {
    # 保留为空，避免破坏现有代码
}


# 默认 Task 配置模板 (已废弃 - 请使用 task_manager.py 中的 PROFESSIONAL_TASK_CONFIGS)
# @deprecated: 使用 PROFESSIONAL_TASK_CONFIGS 替代
DEFAULT_TASK_CONFIGS = {
    # 保留为空，避免破坏现有代码
}
