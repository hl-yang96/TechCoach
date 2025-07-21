"""
CrewAI 集成模块

这个模块提供了 CrewAI 框架的集成，用于实现自动化 Agentic AI 工作任务。
包含 Agent、Task、Crew 的基础类和管理器。
"""

from .agent_manager import AgentManager
from .task_manager import TaskManager
from .crew_coordinator import CrewCoordinator
from .config import CrewConfig

__all__ = [
    'AgentManager',
    'TaskManager', 
    'CrewCoordinator',
    'CrewConfig'
]
