"""
Crew 协调器

负责协调多个 Agents 和 Tasks，管理整个工作流程。
"""

from os import getenv
from typing import Dict, List, Optional, Any
import logging
from crewai import Crew, Process

from app.agentic_core.llm_router.llm_client import get_llm_client
from app.agentic_core.tools import create_all_tools
from app.agentic_core.rag.config import EMBEDDING_MODEL_NAME_CREW

from .config import CrewConfig
from .agent_manager import AgentManager, PROFESSIONAL_AGENT_CONFIGS, JOB_SEEKER_ANALYST_AGENT, INTERVIEW_QUESTION_EXPERT_AGENT, INDUSTRY_EXPERT_AGENT, JSON_FORMAT_GENERATOR_AGENT
from .task_manager import TaskManager, PROFESSIONAL_TASK_CONFIGS, JOB_SEEKER_ANALYSIS_TASK, TECHNICAL_KNOWLEDGE_OUTLINE_TASK, INTERVIEW_QUESTION_BANK_TASK, INTERVIEW_QUESTION_AGGREGATE_TASK,GENERATE_OUTLINE_RESULT_TASK


logger = logging.getLogger(__name__)

DOMAIN_KNOWLEDGE_OUTLINE_GENERATE_CREW = "domain_knowledge_outline_generate_crew"
QUESTION_GENERATE_CREW = "question_generate_crew"

GLOBAL_CREW_CONFIG = {
    DOMAIN_KNOWLEDGE_OUTLINE_GENERATE_CREW: CrewConfig(
        name="特定领域知识点生成",
        description="该 Crew 能够根据求职者的背景和技能，系统性地生成相关的技术知识点大纲。",
        process="sequential",  # sequential, hierarchical
        agents=[
            JOB_SEEKER_ANALYST_AGENT,
            INDUSTRY_EXPERT_AGENT,
            JSON_FORMAT_GENERATOR_AGENT
        ],
        tasks=[
            JOB_SEEKER_ANALYSIS_TASK,
            TECHNICAL_KNOWLEDGE_OUTLINE_TASK,
            GENERATE_OUTLINE_RESULT_TASK,
        ],
        memory=False,
        verbose=True
    ),


    QUESTION_GENERATE_CREW: CrewConfig(
        name="面试题库生成",
        description="该 Crew 通过分析给出的具体知识点，求职者的数据等信息，生成特定技术领域的全面、准确且个性化的面试题库。",
        # process="hierarchical",
        # manager_llm=get_llm_client().get_base_crew_client(),
        process="sequential",  # sequential, hierarchical
        agents=[
            JOB_SEEKER_ANALYST_AGENT,
            INDUSTRY_EXPERT_AGENT,
            INTERVIEW_QUESTION_EXPERT_AGENT,
            JSON_FORMAT_GENERATOR_AGENT],
        tasks=[
            JOB_SEEKER_ANALYSIS_TASK,
            INTERVIEW_QUESTION_BANK_TASK,
            INTERVIEW_QUESTION_AGGREGATE_TASK
        ],
        memory=False,
        verbose=True
    )

}

class CrewCoordinator:
    """Crew 协调器类"""
    
    def __init__(self,
                 agent_manager: Optional[AgentManager] = None,
                 task_manager: Optional[TaskManager] = None):
        self.agent_manager = agent_manager or AgentManager()
        self.task_manager  = task_manager  or TaskManager()
        self.crews: Dict[str, Crew] = {}
        self.crew_configs: Dict[str, CrewConfig] = {}

    def create_crew(self, crew_type: str) -> Crew:
        try:
            crew_config = GLOBAL_CREW_CONFIG.get(crew_type) 
             
            # create tools map
            tools = create_all_tools()
            
            # create agent
            agents = [self.agent_manager.create_professional_agent(agent_name, tools) for agent_name in crew_config.agents]
 
            # create tasks
            tasks = [self.task_manager.create_task(task_name, agents) for task_name in crew_config.tasks]
            
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

            logger.info(f"Created crew: {crew_config.name}")
            return crew
            
        except Exception as e:
            logger.error(f"Failed to create crew {crew_config.name}: {str(e)}")
            raise
    
    def _get_default_manager_llm(self) -> Any:
        return get_llm_client().get_base_crew_client()
