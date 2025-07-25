"""
Task 管理器

负责创建、配置和管理 CrewAI Tasks。
"""

from typing import Dict, List, Optional, Any
import logging
from crewai import Task, Agent

from .config import TaskConfig


logger = logging.getLogger(__name__)

JOB_SEEKER_ANALYSIS_TASK         = "job_seeker_analysis"
TECHNICAL_KNOWLEDGE_OUTLINE_TASK = "technical_knowledge_outline"
GENERATE_OUTLINE_RESULT_TASK     = "generate_knowledge_outline"
INTERVIEW_QUESTION_BANK_TASK      = "interview_question_bank"
INTERVIEW_QUESTION_AGGREGATE_TASK = "interview_question_aggregate"


# 专业 Task 配置 - 基于具体业务需求设计
PROFESSIONAL_TASK_CONFIGS = {
    JOB_SEEKER_ANALYSIS_TASK: TaskConfig(
        name=JOB_SEEKER_ANALYSIS_TASK,
        description="请你对求职者的背景信息进行深入分析，生成一份结构化总结。该分析将被用于后续生成针对性的面试题库，因此除了基础资料外，请重点提取该求职者的技术栈、项目经历、能力优势与知识盲区等信息。主要的数据来源是向量数据库，你需要使用工具来获得足够的信息。",
        expected_output="""一段简洁有力且丰富全面的分析结果，以文本形式输出，以下是示例格式：:
工作年限: 5年
工作职位: 电商行业 高级后端开发工程师
求职目标: 寻找高级后端开发岗位，尤其是涉及电商，高并发等...，与个人项目经验比较相符
项目经验:  
- 项目1: 基于微服务架构的电商平台，负责订单服务模块的设计与实现，使用 Spring Boot 和 Docker...
- 项目2: 实时数据处理系统，使用 Apache Kafka 和 Spark Streaming 进行数据流处理，并且...
- ...
技术栈:
- Java, Spring Boot, Docker, Kubernetes, MySQL, Redis
- 熟悉微服务架构和分布式系统设计
- ...
能力优势:
- 扎实的 Java 编程能力，熟悉 Spring Boot 框架
- 丰富的微服务架构设计经验，能够独立完成复杂模块的开发
- 熟悉容器化技术，能够在 Kubernetes 上部署和管理应用
- ...
知识弱区: （尤其是未来求职目标 上的知识较弱的部分）
- 对于高并发系统的优化经验较少
...
""",
        agent_role="资深职业咨询师"
    ),

    TECHNICAL_KNOWLEDGE_OUTLINE_TASK: TaskConfig(
        name=TECHNICAL_KNOWLEDGE_OUTLINE_TASK,
        description="""请你为 {domain} 这个知识领域生成一份完整且结构清晰的知识大纲，用于该求职者的面试准备，要求如下：
- 大纲应该分为两个层级，一级知识点为大类，二级更加细分的知识点。
- 大纲中的知识点系统性强，全面覆盖求职者在此知识领域的所需的知识范围，求职者将按照这个思路进行知识复习与面试准备。
- 包含从基础到进阶的内容，从基础到拔高的知识点，确保求职者能够全面了解该领域的知识体系，且在面试中具有一些亮点。
- 根据求职者的背景、项目经历、求职目标等特点，有针对性地进行知识点的选择：对于项目、背景、求职目标的相关性高的细分知识点可以相对详细。而对于相关性较弱的可以相对简略。
- 可以适当添加 10%～20 与求职者过往经历和业务场景相结合的知识点，作为面试中的差异化与亮点。
- 如果求职者的求职目标与过往背景和项目经历不符合，请主要聚焦于未来的求职目标的发展方向，生成相关的知识点。
- 该大纲将用于面试题检索、学习路径规划等下游任务，因此请注意层次分明、逻辑清晰、语言准确。
""",
        expected_output="""以 markdown 输出即可：
xxxx领域知识大纲
1. （一级知识点）
  -  (二级知识点)
  - ...
2. ...
...
备注：可以适当阐述你的思路，比如“包含一些针对求职者背景的知识点”，“针对面试中的差异化与亮点进行了思考” 之类的。
""",
        context=[JOB_SEEKER_ANALYSIS_TASK],
        agent_role="行业知识专家"
    ),

    GENERATE_OUTLINE_RESULT_TASK: TaskConfig(
        name=GENERATE_OUTLINE_RESULT_TASK,
        description="""请你将之前生成的知识大纲进行格式化处理，输出为 JSON 格式的结构化对象，包含以下字段：
- domain: 知识领域名称
- comments: 备注信息，包含技术大纲的特点，是否生成了针对求职者背景的知识点。
- outline: 知识大纲内容，为一个数组，其中每个节点包含一级知识点 name, 以及二级知识点的原始文本 content。
""",
        expected_output="""
{
    "domain": "操作系统",
    "comments": "本文包含了针对求职者背景生成的操作系统的知识大纲...",
    "outline": [
        {   
            "name": "进程与线程管理",
            "content": "所有二级知识点"
        },
        {
            "name": "内存管理",
            "content": "所有二级知识点"
        },
    ]
}
""",
        context=[TECHNICAL_KNOWLEDGE_OUTLINE_TASK],
        agent_role="JSON 格式转换大师"
    ),

    INTERVIEW_QUESTION_BANK_TASK: TaskConfig(
        name=INTERVIEW_QUESTION_BANK_TASK,
        description="""根据求职者的背景信息,以及为其量身定制的技术领域的知识大纲，生成尽可能全面的面试题库。

求职者背景信息：{JobSeekerAnalysisResult}

相关技术领域：{domain}
知识点大纲：{Outline}
备注：{Comment}

要求：
- 要求题目基于知识大纲中的知识点依次生成，针对每个小知识点都生成适量的题目，数量主要依据知识点的大小以及面试中的常见程度，知识点内容多并且在面试中常见的，可以适当增加题目数量，反之减少。
- 考虑求职者的工作年限和职业背景，分析每个知识点对于求职者来说的关联程度，从而生成难度适宜的题目，并且可以考虑循序渐进地提问，从浅到深能够探索求职者的知识边界。
- 生成的题目中，10%~20%的题目可以与求职者的以往项目经历、技术栈，以及未来求职目标进行关联，以便更好地模拟真实面试的题目场景。
""",
        expected_output="""
技术领域知识点：
- 知识点1
  1. 问题1
  2. 问题2
- ...
""",
        context=[JOB_SEEKER_ANALYSIS_TASK],
        agent_role="面试题库生成专家"
    ),

    INTERVIEW_QUESTION_AGGREGATE_TASK: TaskConfig(
        name=INTERVIEW_QUESTION_AGGREGATE_TASK,
        description="""请你将之前生成的所有面试题库进行整合，确保题目覆盖全面且无重复。
要求：
- 确保题目之间没有重复，且每个二级知识点至少有一个题目。
- 输出格式为结构化 JSON 对象，包含一个字段 questions 列表，每个题目包含内容content，以及 difficulty=[easy,medium,hard]。
""",
        expected_output="""{
questions: [
    {"content": "什么是进程和线程？", "difficulty": "easy"},
    {"content": "docker run 容器时，Linux 内核是如何利用这两项技术为容器创建一个隔离的运行环境的。", "difficulty": "medium"},
    ...
]}
""",
        context=[INTERVIEW_QUESTION_BANK_TASK],
        agent_role="JSON 格式转换大师"
    )
}


class TaskManager:
    """Task 管理器类"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_configs: Dict[str, TaskConfig] = {}
        self.task_dependencies: Dict[str, List[str]] = {}

    def create_task(self, task_type: str, agents: List[Agent], tools: Optional[List[Any]] = None) -> Task:
        try:
            task_config = PROFESSIONAL_TASK_CONFIGS.get(task_type)
            if not task_config:
                logger.error(f"Unknown professional task type: {task_type}")
                raise ValueError(f"Unknown task type: {task_type}")
                        
            agent = None
            for a in agents:
                    if a.role.lower().replace(" ", "_") == task_config.agent_role.lower().replace(" ", "_"):
                        agent = a
                        break
            if agent is None:
                raise ValueError(f"No agent found for role: {task_config.agent_role}")
                
            context_tasks = []
            if task_config.context:
                for context_key in task_config.context:
                    context_task = self.get_task(context_key)
                    if context_task:
                        context_tasks.append(context_task)
            
            # 创建 Task
            task = Task(
                description=task_config.description,
                expected_output=task_config.expected_output,
                agent=agent,
                tools=tools or [],
                context=context_tasks or [],
                output_file=task_config.output_file
            )
            
            # 存储 Task 和配置
            self.tasks[task_config.name] = task
            self.task_configs[task_config.name] = task_config
            
            # 记录依赖关系
            if context_tasks:
                context_keys = []
                for ctx_task in context_tasks:
                    # 查找上下文任务的键名
                    for key, stored_task in self.tasks.items():
                        if stored_task == ctx_task:
                            context_keys.append(key)
                            break
                self.task_dependencies[task_config.name] = context_keys
                logger.info(f"Task {task_config.name} depends on: {context_keys}")
            
            logger.info(f"Created task: {task_config.name}")
            return task
            
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            raise
    
    def list_professional_task_types(self) -> List[str]:
        """列出所有专业 Task 类型"""
        return list(PROFESSIONAL_TASK_CONFIGS.keys())

    def get_task(self, task_key: str) -> Optional[Task]:
        return self.tasks.get(task_key)
    
    def list_tasks(self) -> List[str]:
        return list(self.tasks.keys())
    
    def get_task_dependencies(self, task_key: str) -> List[str]:
        return self.task_dependencies.get(task_key, [])
    
    def remove_task(self, task_key: str) -> bool:
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
        result = []
        for task_key, config in self.task_configs.items():
            if config.agent_role == agent_role:
                result.append(task_key)
        return result
    
    def _generate_task_key(self, description: str) -> str:
        # 简化描述作为键名
        key = description.lower().replace(" ", "_")[:50]
        
        # 确保键名唯一
        counter = 1
        original_key = key
        while key in self.tasks:
            key = f"{original_key}_{counter}"
            counter += 1
            
        return key
