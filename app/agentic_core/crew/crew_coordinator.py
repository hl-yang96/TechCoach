"""
Crew 协调器

负责协调多个 Agents 和 Tasks，管理整个工作流程。
"""

from os import getenv
from typing import Dict, List, Optional, Any
import logging
from crewai import Crew, Process

from app.agentic_core.llm_router.llm_client import get_llm_client
from app.agentic_core.tools.vector_search_tool import VectorSearchTool, new_vector_search_tool
from app.agentic_core.rag.config import EMBEDDING_MODEL_NAME_CREW

from .config import CrewConfig
from .agent_manager import AgentManager, PROFESSIONAL_AGENT_CONFIGS, JOB_SEEKER_ANALYST_AGENT, INTERVIEW_QUESTION_EXPERT_AGENT, INDUSTRY_EXPERT_AGENT
from .task_manager import TaskManager, PROFESSIONAL_TASK_CONFIGS, JOB_SEEKER_ANALYSIS_TASK, TECHNICAL_KNOWLEDGE_OUTLINE_TASK, INTERVIEW_QUESTION_BANK_TASK


logger = logging.getLogger(__name__)

QUESTION_GENERATE_CREW = "question_generate_crew"

GLOBAL_CREW_CONFIG = {
    QUESTION_GENERATE_CREW: CrewConfig(
        name="特定领域面试题库生成 Crew",
        description="该 Crew 负责生成特定技术领域的面试题库，包含多个任务，依次执行求职者背景分析、知识大纲生成和面试题库生成。",
        process="sequential",
        agents=[PROFESSIONAL_AGENT_CONFIGS.get(JOB_SEEKER_ANALYST_AGENT),
            PROFESSIONAL_AGENT_CONFIGS.get(INDUSTRY_EXPERT_AGENT),
            PROFESSIONAL_AGENT_CONFIGS.get(INTERVIEW_QUESTION_EXPERT_AGENT)
        ],
        tasks=[JOB_SEEKER_ANALYSIS_TASK,
            TECHNICAL_KNOWLEDGE_OUTLINE_TASK,
            INTERVIEW_QUESTION_BANK_TASK
        ],
        memory=False
    )

}

class CrewCoordinator:
    """Crew 协调器类"""
    
    def __init__(self,
                 agent_manager: Optional[AgentManager] = None,
                 task_manager: Optional[TaskManager] = None):
        self.agent_manager = agent_manager or AgentManager()
        self.task_manager = task_manager or TaskManager()
        self.crews: Dict[str, Crew] = {}
        self.crew_configs: Dict[str, CrewConfig] = {}

    async def create_question_generation_crew(self, domain: str) -> Optional[Crew]:
        """创建面试题生成 Crew"""
        try:
            crew_config = GLOBAL_CREW_CONFIG.get(QUESTION_GENERATE_CREW)
            
            # create tools
            vector_search_tool = await new_vector_search_tool()
            tools = [vector_search_tool]
            
            # create agent
            agents = [self.agent_manager.create_agent(agent_config,tools) for agent_config in crew_config.agents]
 
            # create tasks
            tasks = [self.task_manager.professional_task_factory(task_type, agents, domain=domain) for task_type in crew_config.tasks]
            
            # create Crew
            crew = self.create_crew(crew_config, agents, tasks)
            return crew

        except Exception as e:
            logger.error(f"创建面试题生成 Crew 失败: {str(e)}")
            return None

    async def execute_question_generation_crew(self, domain: str) -> Dict[str, Any]:
        """执行面试题生成工作流程"""
        try:
            # 创建 Crew
            crew = await self.create_question_generation_crew(domain)
            if not crew:
                return {"error": "创建 Crew 失败", "status": "error"}

            # 执行 Crew
            result = crew.kickoff()

            return {
                "status": "success",
                "result": result,
                "domain": domain
            }

        except Exception as e:
            logger.error(f"执行面试题生成工作流程失败: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "domain": domain
            }
        
    def create_crew(self, crew_config: CrewConfig, agents, tasks) -> Crew:
        try:
            process = Process.sequential
            if crew_config.process == "hierarchical":
                process = Process.hierarchical
            
            crew_kwargs = {
                "agents": agents, "tasks": tasks,
                "verbose": crew_config.verbose, "memory": crew_config.memory, "process": process
            }
            
            if crew_config.process == "hierarchical":
                manager_llm = crew_config.manager_llm or self._get_default_manager_llm()
                crew_kwargs["manager_llm"] = manager_llm
            
            if crew_config.memory:
                crew_kwargs["embedder"] = {"provider": "google", "config":{"api_key": getenv("GEMINI_API_KEY"), "model": EMBEDDING_MODEL_NAME_CREW}}

            crew = Crew(**crew_kwargs)
            crew_key = crew_config.name.lower().replace(" ", "_")
            self.crews[crew_key] = crew
            self.crew_configs[crew_key] = crew_config
            
            logger.info(f"Created crew: {crew_config.name}")
            return crew
            
        except Exception as e:
            logger.error(f"Failed to create crew {crew_config.name}: {str(e)}")
            raise
    
    def get_crew(self, crew_key: str) -> Optional[Crew]:
        return self.crews.get(crew_key)
    
    def execute_crew(self, crew_key: str, inputs: Optional[Dict[str, Any]] = None) -> Any:
        crew = self.get_crew(crew_key)
        if crew is None:
            raise ValueError(f"Crew not found: {crew_key}")
        
        try:
            logger.info(f"Starting execution of crew: {crew_key}")
            if inputs:
                result = crew.kickoff(inputs=inputs)
            else:
                result = crew.kickoff()
            logger.info(f"Completed execution of crew: {crew_key}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute crew {crew_key}: {str(e)}")
            raise
    
    def list_crews(self) -> List[str]:
        return list(self.crews.keys())
    
    def remove_crew(self, crew_key: str) -> bool:
        if crew_key in self.crews:
            del self.crews[crew_key]
            del self.crew_configs[crew_key]
            logger.info(f"Removed crew: {crew_key}")
            return True
        return False
    
    def get_crew_info(self, crew_key: str) -> Optional[Dict[str, Any]]:
        if crew_key not in self.crews:
            return None
        # crew = self.crews[crew_key]

        config = self.crew_configs[crew_key]
        return {
            "key": crew_key,
            "name": config.name,
            "description": config.description,
            "process": config.process,
            "verbose": config.verbose,
            "memory": config.memory,
            "agents_count": len(config.agents),
            "tasks_count": len(config.tasks),
            "agent_roles": [agent.role for agent in config.agents],
            "task_descriptions": [task.description[:100] + "..." if len(task.description) > 100 
                                else task.description for task in config.tasks]
        }
    
    def create_simple_crew(self, 
                          name: str,
                          description: str,
                          agent_roles: List[str],
                          task_descriptions: List[str],
                          process: str = "sequential") -> Crew:
        from .config import AgentConfig, TaskConfig
        crew_config = CrewConfig(
            name=name,
            description=description,
            process=process
        )
        
        for role in agent_roles:
            agent_config = AgentConfig(
                role=role,
                goal=f"Complete tasks as a {role}",
                backstory=f"You are an expert {role} with extensive experience."
            )
            crew_config.add_agent(agent_config)
        
        for i, task_desc in enumerate(task_descriptions):
            agent_role = agent_roles[i % len(agent_roles)]  # 循环分配
            task_config = TaskConfig(
                description=task_desc,
                expected_output="A comprehensive and detailed response",
                agent_role=agent_role
            )
            crew_config.add_task(task_config)
        
        return self.create_crew(crew_config)
    
    def _get_default_manager_llm(self) -> Any:
        return get_llm_client().get_base_crew_client()
