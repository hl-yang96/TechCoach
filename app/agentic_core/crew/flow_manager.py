import json
import sys
from typing import Any, Dict, List
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from app.agentic_core.crew.crew_coordinator import CrewCoordinator, DOMAIN_KNOWLEDGE_OUTLINE_GENERATE_CREW, QUESTION_GENERATE_CREW
import logging

from app.agentic_core.crew.task_manager import JOB_SEEKER_ANALYSIS_TASK

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateDomainKnowledgeQuestionState(BaseModel):
    job_seeker_analysis_result: str = ""
    domain: str = ""
    comments: str = ""
    outline: List[Dict[str, Any]] = []

class GenerateDomainKnowledgeQuestionFlow(Flow[GenerateDomainKnowledgeQuestionState]):
    
    def __init__(self, input_domain: str, persistence = None, **kwargs):
        super().__init__(persistence, **kwargs)
        self.state.domain = input_domain
    
    @start()
    def generate_domain_outline(self):
        try:
            # run the crew to generate domain knowledge outline
            crew_coordinator = CrewCoordinator()
            domain_outline_crew = crew_coordinator.create_crew(DOMAIN_KNOWLEDGE_OUTLINE_GENERATE_CREW)
            if not domain_outline_crew:
                return {"error": "创建领域知识大纲 Crew 失败", "status": "error"}
            crew_result = domain_outline_crew.kickoff(inputs={"domain": self.state.domain})
            
            # process result to state
 
            outline_res = json.loads(crew_result.raw)
            self.state.comments = outline_res["comments"]
            self.state.outline = outline_res["outline"]
            self.state.job_seeker_analysis_result = str(crew_result.tasks_output[0])
            return True
        except Exception as e:
            logger.error(f"生成领域知识大纲失败: {str(e)}")
            raise
        
    @listen(generate_domain_outline)
    def generate_questions(self):
        questions_result = []
        try:
            for item in self.state.outline[:1]:  # TEST
                if not isinstance(item, dict) or "content" not in item or "name" not in item:
                    logger.error(f"Invalid outline item: {item}")
                    return {"error": "知识大纲格式错误", "status": "error"}
                
                name = item.get("name", "")
                content = item.get("content", "")
                if not name or not content:
                    logger.error(f"Outline item missing name or content: {item}")
                    return {"error": "知识大纲项缺少名称或内容", "status": "error"}
                
                # run the crew to generate questions based on the outline
                crew_coordinator = CrewCoordinator()
                question_generate_crew = crew_coordinator.create_crew(QUESTION_GENERATE_CREW)
                if not question_generate_crew:
                    return {"error": "创建面试题库生成 Crew 失败", "status": "error"}
                
                crew_result = question_generate_crew.kickoff(inputs={
                    "JobSeekerAnalysisResult": self.state.job_seeker_analysis_result,
                    "domain": self.state.domain,
                    "Comment": self.state.comments,
                    "Outline": name+"\n"+content
                })
                
                logger.info(f"面试题库生成结果: {crew_result.raw}")
                q_list = json.loads(crew_result.raw)["questions"]
                questions_result.extend(q_list)

            return questions_result
        except Exception as e:
            logger.error(f"生成面试题库失败: {str(e)}")
            raise



