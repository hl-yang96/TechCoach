"""
Agent 管理器

负责创建、配置和管理 CrewAI Agents。
"""

from typing import Dict, List, Optional, Any
import logging
from crewai import Agent
from langchain_openai import ChatOpenAI

from .config import AgentConfig
from ..llm_router.llm_client import LLMClient
from ..tools.vector_search_tool import VectorSearchTool


logger = logging.getLogger(__name__)

PROFESSIONAL_AGENT_CONFIGS = {
    "job_seeker_analyst": AgentConfig(
        # role="Job Seeker Background Analyst",
        role="求职者背景分析师",
        # goal="""You need to conduct a comprehensive understanding and analysis of job seekers, including their work experience, project experience, technical stack and work capabilities, job search goals, career highlights, potential advantages, potential risks, salary levels, etc. Then output a concise, powerful, rich and comprehensive analysis result.""",
        goal="""你需要对求职者做全方位的了解和分析，比如他的过往工作年限，项目经验，技术栈与工作能力，求职目标，职业亮点，潜在优势，潜在风险，工资水平等等。然后输出一段简洁有力且丰富全面的分析结果。""",
        # backstory="""You are an experienced career consultant, especially in the field of Internet technology, and you can accurately analyze your users. At the same time, you also have rich experience in vector retrieval and LlamaIndex RAG. You are good at effectively retrieving documents such as job seekers' resumes, past project records, and learning records from vector knowledge bases, accurately extracting information related to user queries, and returning concise and clear content. You are used to comprehensively obtaining data before analysis, and conducting analysis based on factual data rather than generating out of thin air or making things up.""",
        backstory="""你是一位经验丰富的职业咨询师，尤其是对于互联网技术方面，你能够精准地对你的用户进行分析。同时你还拥有丰富的向量检索和 LlamaIndex RAG 经验，你擅长通过有效检索向量知识库中的求职者简历、过往项目记录、学习记录等文档，准确提取与用户查询相关的信息，并返回简洁清晰的内容。你习惯分析前全面获取数据，并且依据事实数据来进行分析，而不是凭空生成或胡编乱造。""",
        verbose=True,
        allow_delegation=False, # agent could delegate the task to other agent, niubi...
        max_iter=6,
        memory=False, # agent memory, not task context 
        tools=["vector_search"]
    ),

    "interview_question_expert": AgentConfig(
        # role="Interview Question Generation Expert",
        role="面试题库生成专家",
        # goal="""Based on the job seeker's background analysis, generate a rich and comprehensive knowledge question bank that matches the job seeker.""",
        goal="""根据求职者的背景分析，生成符合求职者的且丰富全面的知识题库。""",
        # backstory="""You are an experienced interviewer who has a very deep understanding of interview questions in different fields. You also have rich experience in vector retrieval and LlamaIndex RAG. You are good at effectively retrieving job seekers' resumes, past project records and work experience from vector knowledge bases to gain a deep understanding of job seekers. You can not only generate comprehensive interview question banks for a certain field, but also generate some high-level questions that probe the interviewer's abilities in a simple and profound way based on the job seeker's resume or project experience.""",
        backstory="""你是一位经验丰富的面试官，你能够对不同领域的面试题有非常深入地了解，你还拥有丰富的向量检索和 LlamaIndex RAG 经验，你擅长通过有效地检索向量知识库中的求职者的简历以及过往项目记录和工作经验，对求职者进行深刻地了解。你不仅能够生成某个领域全面的面试题库，还能够针对性地求职者的简历或者项目经历，深入浅出地生成出一些探测面试者能力的有水平的题目。""",
        verbose=True,
        allow_delegation=False, # agent could delegate the task to other agent
        max_iter=6,
        memory=False, # agent memory, not task context
        tools=["vector_search"]
    ),

    "industry_expert": AgentConfig(
        role="行业知识专家",
        goal="""你需要对求职者所在行业以及相关技术领域的知识进行分析和梳理，提取有用的信息，并且全面准确地回答问题，无论是行业技术，面试问题，知识大纲，行业发展等。""",
        backstory="""你是求职者所在行业的专家，你能够对这个行业的技术领域和知识大纲有非常深入地了解，对于某个领域的知识学习也有很深地见解，且对于行业的发展有着很强地前瞻性。同时能够知道不同背景的求职者在面对面试的时候，需要准备哪些知识点。""",
        verbose=True,
        allow_delegation=False,
        max_iter=6,
        memory=False,
        tools=[]  # TODO: 待添加具体工具
    )
}


class AgentManager:

    def __init__(self, llm_client: Optional[LLMClient] = None, auto_initialize: bool = True):
        self.llm_client = llm_client
        self.agents: Dict[str, Agent] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}
        if auto_initialize:
            self.initialize_professional_agents()

    def initialize_professional_agents(self) -> bool:
        try:
            success_count = 0
            vector_search_tool = VectorSearchTool()
            for agent_key, agent_config in PROFESSIONAL_AGENT_CONFIGS.items():
                try:
                    # 为每个 Agent 配置工具
                    tools = [vector_search_tool] if "vector_search" in agent_config.tools else []
                    # 创建 Agent
                    agent = self.create_agent(agent_config, tools)
                    if agent:
                        success_count += 1
                        logger.info(f"Initialized professional agent: {agent_config.role}")
                except Exception as e:
                    logger.error(f"Failed to initialize agent {agent_key}: {str(e)}")

            logger.info(f"Successfully initialized {success_count}/{len(PROFESSIONAL_AGENT_CONFIGS)} professional agents")
            return success_count == len(PROFESSIONAL_AGENT_CONFIGS)

        except Exception as e:
            logger.error(f"Failed to initialize professional agents: {str(e)}")
            return False

    def create_agent(self,
                    agent_config: AgentConfig,
                    tools: Optional[List[Any]] = None,
                    llm: Optional[Any] = None) -> Agent:
        try:
            if llm is None:
                llm = self._get_default_llm()
            
            agent = Agent(
                role=agent_config.role,
                goal=agent_config.goal,
                backstory=agent_config.backstory,
                verbose=agent_config.verbose,
                allow_delegation=agent_config.allow_delegation,
                max_iter=agent_config.max_iter,
                memory=agent_config.memory,
                tools=tools or [],
                llm=llm
            )
            
            # 存储 Agent 和配置
            agent_key = agent_config.role.lower().replace(" ", "_")
            self.agents[agent_key] = agent
            self.agent_configs[agent_key] = agent_config
            
            logger.info(f"Created agent: {agent_config.role}")
            return agent
            
        except Exception as e:
            logger.error(f"Failed to create agent {agent_config.role}: {str(e)}")
            raise
    
    def get_professional_agent(self, agent_type: str) -> Optional[Agent]:
        if agent_type not in PROFESSIONAL_AGENT_CONFIGS:
            logger.error(f"Unknown professional agent type: {agent_type}")
            return None

        # 生成 agent_key
        config = PROFESSIONAL_AGENT_CONFIGS[agent_type]
        agent_key = config.role.lower().replace(" ", "_")

        return self.get_agent(agent_key)

    def get_job_seeker_analyst(self) -> Optional[Agent]:
        return self.get_professional_agent("job_seeker_analyst")

    def get_interview_question_expert(self) -> Optional[Agent]:
        return self.get_professional_agent("interview_question_expert")

    def get_industry_expert(self) -> Optional[Agent]:
        return self.get_professional_agent("industry_expert")

    def list_professional_agents(self) -> List[str]:
        return list(PROFESSIONAL_AGENT_CONFIGS.keys())
    
    def get_agent(self, agent_key: str) -> Optional[Agent]:
        return self.agents.get(agent_key)
    
    def list_agents(self) -> List[str]:
        return list(self.agents.keys())
    
    def remove_agent(self, agent_key: str) -> bool:
        if agent_key in self.agents:
            del self.agents[agent_key]
            del self.agent_configs[agent_key]
            logger.info(f"Removed agent: {agent_key}")
            return True
        return False
    
    def _get_default_llm(self) -> Any:
        try:
            # 如果有 LLM 客户端，尝试使用它
            if self.llm_client:
                # 这里可以根据你的 LLMClient 实现来调整
                # 暂时使用 OpenAI 作为默认
                return ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1
                )
            else:
                # 默认使用 OpenAI
                return ChatOpenAI(
                    model="gpt-3.5-turbo", 
                    temperature=0.1
                )
        except Exception as e:
            logger.warning(f"Failed to create default LLM: {str(e)}")
            # 返回一个基本的 LLM 实例
            return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
    
    def get_agent_info(self, agent_key: str) -> Optional[Dict[str, Any]]:
        """
        获取 Agent 信息

        Args:
            agent_key: Agent 键名

        Returns:
            Agent 信息字典
        """
        if agent_key not in self.agents:
            return None

        config = self.agent_configs[agent_key]

        return {
            "key": agent_key,
            "role": config.role,
            "goal": config.goal,
            "backstory": config.backstory,
            "verbose": config.verbose,
            "allow_delegation": config.allow_delegation,
            "max_iter": config.max_iter,
            "memory": config.memory,
            "tools": config.tools
        }
