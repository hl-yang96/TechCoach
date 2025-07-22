"""
Crew 协调器

负责协调多个 Agents 和 Tasks，管理整个工作流程。
"""

from typing import Dict, List, Optional, Any
import logging
from crewai import Crew, Process

from app.agentic_core.llm_router.llm_client import get_llm_client
from .config import CrewConfig
from .agent_manager import AgentManager
from .task_manager import TaskManager


logger = logging.getLogger(__name__)


class CrewCoordinator:
    """Crew 协调器类"""
    
    def __init__(self, 
                 agent_manager: Optional[AgentManager] = None,
                 task_manager: Optional[TaskManager] = None):
        self.agent_manager = agent_manager or AgentManager()
        self.task_manager = task_manager or TaskManager()
        self.crews: Dict[str, Crew] = {}
        self.crew_configs: Dict[str, CrewConfig] = {}
        
    def create_crew(self, crew_config: CrewConfig) -> Crew:
        try:
            agents = []
            tasks = []
            
            for agent_config in crew_config.agents:
                agent = self.agent_manager.create_agent(agent_config)
                agents.append(agent)
            
            for task_config in crew_config.tasks:
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
                        context_task = self.task_manager.get_task(context_key)
                        if context_task:
                            context_tasks.append(context_task)
                
                task = self.task_manager.create_task(
                    task_config, 
                    agent, 
                    context_tasks=context_tasks
                )
                tasks.append(task)
            
            process = Process.sequential
            if crew_config.process == "hierarchical":
                process = Process.hierarchical
            
            crew_kwargs = {
                "agents": agents, "tasks": tasks,
                "verbose": crew_config.verbose, "memory": crew_config.memory, "process": process
            }
            
            # 如果是层次化流程，需要管理者 LLM
            if crew_config.process == "hierarchical":
                manager_llm = crew_config.manager_llm or self._get_default_manager_llm()
                crew_kwargs["manager_llm"] = manager_llm
            
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
        return get_llm_client().get_base_llm_client()
