"""
Agent 管理器

负责创建、配置和管理 CrewAI Agents。
"""

from typing import Dict, List, Optional, Any
import logging
from crewai import Agent

from .config import AgentConfig
from ..llm_router.llm_client import LLMClient, get_llm_client
from ..tools import TOOL_VECTOR_SEARCH, TOOL_JSON_PARSER, TOOL_READ_FILE, TOOL_GET_EXIST_FILE_LIST

logger = logging.getLogger(__name__)

JOB_SEEKER_ANALYST_AGENT = "job_seeker_analyst"
INTERVIEW_QUESTION_EXPERT_AGENT = "interview_question_expert"
INDUSTRY_EXPERT_AGENT = "industry_expert"
JSON_FORMAT_GENERATOR_AGENT = "json_format_generator"


PROFESSIONAL_AGENT_CONFIGS = {
    JOB_SEEKER_ANALYST_AGENT: AgentConfig(
        # role="Job Seeker Background Analyst",
        role="资深职业咨询师",
        # goal="""You need to conduct a comprehensive understanding and analysis of job seekers, including their work experience, project experience, technical stack and work capabilities, job search goals, career highlights, potential advantages, potential risks, salary levels, etc. Then output a concise, powerful, rich and comprehensive analysis result.""",
        goal="""你会对求职者做全方位的了解和分析，比如他的过往工作年限，项目经验，技术栈与工作能力，求职目标，职业亮点，潜在优势，潜在风险，工资水平等等。""",
        # backstory="""You are an experienced career consultant, especially in the field of Internet technology, and you can accurately analyze your users. At the same time, you also have rich experience in vector retrieval and LlamaIndex RAG. You are good at effectively retrieving documents such as job seekers' resumes, past project records, and learning records from vector knowledge bases, accurately extracting information related to user queries, and returning concise and clear content. You are used to comprehensively obtaining data before analysis, and conducting analysis based on factual data rather than generating out of thin air or making things up.""",
        backstory="""你是一位经验丰富的资深职业咨询师，尤其是对于互联网技术方面，你能够精准地对你的用户进行分析。同时你还拥有丰富的文件检索和向量数据库检索经验，你擅长通过对求职者简历、过往项目记录、学习记录等资料的检索，准确提取与用户查询相关的信息，并返回简洁清晰的内容。你习惯分析前全面获取数据，并且依据事实数据来进行分析，而不是凭空生成或胡编乱造。""",
        verbose=True,
        allow_delegation=False, # agent could delegate the task to other agent, niubi...
        max_iter=5,
        memory=False, # agent memory, not task context 
        tools=[TOOL_VECTOR_SEARCH]  # 使用向量检索工具和文件读取工具来获取求职者的背景信息
    ),

    INDUSTRY_EXPERT_AGENT: AgentConfig(
        role="行业知识专家",
        goal="""你需要对求职者所在行业以及相关技术领域的知识进行分析和梳理，提取有用的信息，并且全面准确地回答问题，无论是行业技术，面试问题，知识大纲，行业发展等。""",
        backstory="""你是求职者所在行业的专家，你能够对这个行业的技术领域和知识大纲有非常深入地了解，对于某个领域的知识学习也有很深地见解，且对于行业的发展有着很强地前瞻性。同时能够知道不同背景的求职者在面对面试的时候，需要准备哪些知识点。""",
        verbose=True,
        allow_delegation=False,
        max_iter=2,
        memory=False,
        tools=[]  # TODO: 待添加具体工具
    ),

    INTERVIEW_QUESTION_EXPERT_AGENT: AgentConfig(
        # role="Interview Question Generation Expert",
        role="面试题库生成专家",
        # goal="""Based on the job seeker's background analysis, generate a rich and comprehensive knowledge question bank that matches the job seeker.""",
        goal="""根据求职者的背景分析，生成符合求职者的且丰富全面的知识题库。""",
        # backstory="""You are an experienced interviewer who has a very deep understanding of interview questions in different fields. You also have rich experience in vector retrieval and LlamaIndex RAG. You are good at effectively retrieving job seekers' resumes, past project records and work experience from vector knowledge bases to gain a deep understanding of job seekers. You can not only generate comprehensive interview question banks for a certain field, but also generate some high-level questions that probe the interviewer's abilities in a simple and profound way based on the job seeker's resume or project experience.""",
        backstory="""你是一位经验丰富的面试官，你能够对不同领域的面试题有非常深入地了解，你不仅能够生成某个领域全面的面试题库，还能够针对性地求职者的简历或者项目经历，深入浅出地生成出一些探测面试者能力的有水平的题目。""",
        verbose=True,
        allow_delegation=True, # agent could delegate the task to other agent
        max_iter=5,
        memory=False, # agent memory, not task context
        tools=[TOOL_VECTOR_SEARCH]
    ),
    
    JSON_FORMAT_GENERATOR_AGENT: AgentConfig(
        role="JSON 格式生成大师",
        goal="""你需要将提供的内容按照要求转换为符合要求的 JSON 格式，以便于后续处理和使用。""",
        backstory="""你是一个经验丰富的 JSON 格式生成大师，你能严格遵循 Task 任务的具体需求，将复杂的内容转换为结构化的 JSON 格式，你能够确保生成的 JSON 数据符合规范，并且生成的结果中不包括任何多余的内容，也不要markdown的代码块等格式。""",
        verbose=True,
        allow_delegation=False,
        max_iter=2,
        memory=False,
        tools=[]  # 使用 JSON 解析工具来验证生成的 JSON 格式是否正确，但是会导致上下文过大好像...
    )
}

class AgentManager:

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or get_llm_client().get_base_crew_client()
        self.agents: Dict[str, Agent] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}

    def create_agent(self,
                    agent_config: AgentConfig,
                    tools: Optional[List[Any]] = None,
                    llm: Optional[Any] = None) -> Agent:
        try:
            final_tools = []
            for tool_name in agent_config.tools:
                tool = tools.get(tool_name) if tools else None
                if tool:
                    final_tools.append(tool)
                else:
                    logger.warning(f"Tool {tool_name} not found for agent {agent_config.role}")
            
            agent = Agent(
                role=agent_config.role,
                goal=agent_config.goal,
                backstory=agent_config.backstory,
                verbose=agent_config.verbose,
                allow_delegation=agent_config.allow_delegation,
                max_iter=agent_config.max_iter,
                memory=agent_config.memory,
                tools=final_tools,
                llm=llm or self.llm_client
            )
            
            logger.info(f"Created agent: {agent_config.role}")
            return agent
            
        except Exception as e:
            logger.error(f"Failed to create agent {agent_config.role}: {str(e)}")
            raise

    def create_professional_agent(self, agent_type: str, tools: Optional[List[Any]] = None, llm: Optional[Any] = None) -> Optional[Agent]:
        if agent_type not in PROFESSIONAL_AGENT_CONFIGS:
            logger.error(f"Unknown agent type: {agent_type}")
            return None
        
        agent_config = PROFESSIONAL_AGENT_CONFIGS[agent_type]
        return self.create_agent(agent_config, tools, llm)