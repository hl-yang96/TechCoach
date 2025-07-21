"""
Task 管理器

负责创建、配置和管理 CrewAI Tasks。
"""

from typing import Dict, List, Optional, Any
import logging
from crewai import Task, Agent

from .config import TaskConfig


logger = logging.getLogger(__name__)


# 专业 Task 配置 - 基于具体业务需求设计
PROFESSIONAL_TASK_CONFIGS = {
    "job_seeker_analysis": TaskConfig(
        description="请你对求职者的背景信息进行深入分析，生成一份结构化总结。该分析将被用于后续生成针对性的技术题库，且关注的技术领域是{Domain}，因此请重点提取该求职者的技术栈、项目经历、能力优势与知识盲区等信息。",
        expected_output="""一段简洁有力且丰富全面的分析结果，以文本形式输出:
工作年限:
项目经验:
技术栈:
能力优势:
知识盲区:
...""",
        agent_role="求职者背景分析师"
    ),

    "technical_knowledge_outline": TaskConfig(
        description="请你根据求职者的背景、项目经历和求职目标等特点，为其在 {Domain} 这个技术领域生成一份完整且结构清晰的知识大纲，用于该求职者的面试准备，不用生成具体题目，大纲简洁全面且完整包含求职者需要掌握的内容。该大纲应涵盖该领域从基础到进阶的重要知识点和面试考点。该大纲将用于指导出题 Agent、学习路径规划 Agent 等下游任务，因此请注意层次分明、逻辑清晰、语言准确。",
        expected_output="""Markdown 格式的技术知识大纲文档，包含以下结构：
1. 核心知识体系概览(列表)
2. 各模块知识点展开(列表)
  - 2.1 子领域A
    - 知识点1
    - 知识点2
  - 2.2 子领域B
    - 知识点
3. 行业发展趋势与新技术动态(可选)""",
        agent_role="行业知识专家"
    ),

    "interview_question_bank": TaskConfig(
        description="""根据之前的任务提供 求职者的背景信息 以及技术领域的知识大纲（来自 Task2），为 {Domain} 这个技术领域生成一个尽可能全面的面试题库。
要求：
- 题目需基于知识大纲中的知识点生成；知识大纲若有遗漏，应适当补充该领域常见知识点；
- 每个知识点题目确保覆盖全面，且面试中可能会遇到；
- 题目仅包括题干，无需答案或其他字段；输出为结构化 JSON 对象，仅包含一个字段 questions，其值为题目字符串列表；""",
        expected_output="""{
  "questions": [
    "问题1",
    "问题2",
    ...
  ]
}""",
        agent_role="面试题库生成专家"
    )
}


class TaskManager:
    """Task 管理器类"""

    def __init__(self, auto_initialize: bool = False):
        """
        初始化 Task 管理器

        Args:
            auto_initialize: 是否自动初始化专业 Task 配置
        """
        self.tasks: Dict[str, Task] = {}
        self.task_configs: Dict[str, TaskConfig] = {}
        self.task_dependencies: Dict[str, List[str]] = {}
        self.professional_task_configs = PROFESSIONAL_TASK_CONFIGS.copy()

        # 可选择自动初始化专业 Task 配置
        if auto_initialize:
            self.initialize_professional_task_configs()

    def initialize_professional_task_configs(self) -> bool:
        """
        初始化专业 Task 配置到本地存储

        Returns:
            是否成功初始化
        """
        try:
            for task_key, task_config in PROFESSIONAL_TASK_CONFIGS.items():
                # 将专业 task 配置存储到本地配置中
                self.task_configs[task_key] = task_config
                logger.info(f"Initialized professional task config: {task_key}")

            logger.info(f"Successfully initialized {len(PROFESSIONAL_TASK_CONFIGS)} professional task configs")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize professional task configs: {str(e)}")
            return False

    def get_professional_task_config(self, task_type: str) -> Optional[TaskConfig]:
        """
        获取专业 Task 配置

        Args:
            task_type: Task 类型 ("job_seeker_analysis", "technical_knowledge_outline", "interview_question_bank")

        Returns:
            TaskConfig 实例或 None
        """
        return PROFESSIONAL_TASK_CONFIGS.get(task_type)

    def create_professional_task(self,
                                task_type: str,
                                agent: Agent,
                                domain: str = "",
                                tools: Optional[List[Any]] = None,
                                context_tasks: Optional[List[Task]] = None) -> Optional[Task]:
        """
        从专业配置创建 Task

        Args:
            task_type: Task 类型
            agent: 执行任务的 Agent
            domain: 技术领域（用于模板替换）
            tools: 工具列表
            context_tasks: 上下文任务列表

        Returns:
            创建的 Task 实例或 None
        """
        task_config = self.get_professional_task_config(task_type)
        if not task_config:
            logger.error(f"Unknown professional task type: {task_type}")
            return None

        # 替换模板变量
        if domain:
            # 创建配置副本以避免修改原始配置
            task_config_copy = TaskConfig(
                description=task_config.description.format(Domain=domain, domain=domain),
                expected_output=task_config.expected_output,
                agent_role=task_config.agent_role,
                tools=task_config.tools.copy() if task_config.tools else [],
                context=task_config.context.copy() if task_config.context else None,
                output_file=task_config.output_file
            )
        else:
            task_config_copy = task_config

        return self.create_task(task_config_copy, agent, tools, context_tasks)

    def create_task(self,
                   task_config: TaskConfig,
                   agent: Agent,
                   tools: Optional[List[Any]] = None,
                   context_tasks: Optional[List[Task]] = None) -> Task:
        """
        创建一个新的 Task
        
        Args:
            task_config: Task 配置
            agent: 执行任务的 Agent
            tools: 工具列表
            context_tasks: 上下文任务列表（依赖的任务）
            
        Returns:
            创建的 Task 实例
        """
        try:
            # 创建 Task
            task = Task(
                description=task_config.description,
                expected_output=task_config.expected_output,
                agent=agent,
                tools=tools or [],
                context=context_tasks or [],
                output_file=task_config.output_file
            )
            
            # 生成任务键名
            task_key = self._generate_task_key(task_config.description)
            
            # 存储 Task 和配置
            self.tasks[task_key] = task
            self.task_configs[task_key] = task_config
            
            # 记录依赖关系
            if context_tasks:
                context_keys = []
                for ctx_task in context_tasks:
                    # 查找上下文任务的键名
                    for key, stored_task in self.tasks.items():
                        if stored_task == ctx_task:
                            context_keys.append(key)
                            break
                self.task_dependencies[task_key] = context_keys
            
            logger.info(f"Created task: {task_key}")
            return task
            
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            raise
    
    def list_professional_task_types(self) -> List[str]:
        """列出所有专业 Task 类型"""
        return list(PROFESSIONAL_TASK_CONFIGS.keys())

    def get_professional_task_info(self, task_type: str) -> Optional[Dict[str, Any]]:
        """
        获取专业 Task 信息

        Args:
            task_type: Task 类型

        Returns:
            Task 信息字典
        """
        task_config = self.get_professional_task_config(task_type)
        if not task_config:
            return None

        return {
            "type": task_type,
            "description": task_config.description,
            "expected_output": task_config.expected_output,
            "agent_role": task_config.agent_role,
            "tools": task_config.tools,
            "context": task_config.context,
            "output_file": task_config.output_file
        }
    
    def get_task(self, task_key: str) -> Optional[Task]:
        """
        获取已创建的 Task
        
        Args:
            task_key: Task 键名
            
        Returns:
            Task 实例或 None
        """
        return self.tasks.get(task_key)
    
    def list_tasks(self) -> List[str]:
        """
        列出所有已创建的 Task
        
        Returns:
            Task 键名列表
        """
        return list(self.tasks.keys())
    
    def get_task_dependencies(self, task_key: str) -> List[str]:
        """
        获取任务依赖关系
        
        Args:
            task_key: Task 键名
            
        Returns:
            依赖的任务键名列表
        """
        return self.task_dependencies.get(task_key, [])
    
    def remove_task(self, task_key: str) -> bool:
        """
        移除 Task
        
        Args:
            task_key: Task 键名
            
        Returns:
            是否成功移除
        """
        if task_key in self.tasks:
            del self.tasks[task_key]
            del self.task_configs[task_key]
            if task_key in self.task_dependencies:
                del self.task_dependencies[task_key]
            
            # 移除其他任务对此任务的依赖
            for _, deps in self.task_dependencies.items():
                if task_key in deps:
                    deps.remove(task_key)
            
            logger.info(f"Removed task: {task_key}")
            return True
        return False
    
    def get_task_info(self, task_key: str) -> Optional[Dict[str, Any]]:
        """
        获取 Task 信息
        
        Args:
            task_key: Task 键名
            
        Returns:
            Task 信息字典
        """
        if task_key not in self.tasks:
            return None

        config = self.task_configs[task_key]
        dependencies = self.task_dependencies.get(task_key, [])
        
        return {
            "key": task_key,
            "description": config.description,
            "expected_output": config.expected_output,
            "agent_role": config.agent_role,
            "tools": config.tools,
            "output_file": config.output_file,
            "dependencies": dependencies
        }
    
    def get_tasks_by_agent(self, agent_role: str) -> List[str]:
        """
        获取指定 Agent 的所有任务
        
        Args:
            agent_role: Agent 角色
            
        Returns:
            Task 键名列表
        """
        result = []
        for task_key, config in self.task_configs.items():
            if config.agent_role == agent_role:
                result.append(task_key)
        return result
    
    def _generate_task_key(self, description: str) -> str:
        """
        生成任务键名
        
        Args:
            description: 任务描述
            
        Returns:
            任务键名
        """
        # 简化描述作为键名
        key = description.lower().replace(" ", "_")[:50]
        
        # 确保键名唯一
        counter = 1
        original_key = key
        while key in self.tasks:
            key = f"{original_key}_{counter}"
            counter += 1
            
        return key
