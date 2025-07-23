"""
Interview Question Management Router
File: app/gateway/routers/question.py
Created: 2025-07-17
Purpose: question generation and management
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.shared_kernel.database_service import TechDomainDBService, TechDomainQuestionDBService
from app.question_service.service import tech_domain_service, tech_question_service
from app.agentic_core.crew.crew_coordinator import CrewCoordinator

router = APIRouter()
db_service = TechDomainDBService()
question_db_service = TechDomainQuestionDBService()

######################################### Tech Domain ########################################

class TechDomainCreateRequest(BaseModel):
    name: str

class TechDomainResponse(BaseModel):
    name: str

class TechDomainsListResponse(BaseModel):
    domains: List[TechDomainResponse]

class TechDomainCreateResponse(BaseModel):
    name: str
    message: str

class TechDomainDeleteRequest(BaseModel):
    name: str

class TechDomainDeleteResponse(BaseModel):
    message: str
    status: str
    name: str

@router.post("/tech-domains/generate", response_model=TechDomainsListResponse)
async def generate_tech_domains():
    """
    Generate dynamic tech domains based on user's profile and context
    存储到数据库后返回结果
    """
    try:
        # 使用硬编码的上下文和真实的LLM生成
        
        domains = tech_domain_service.generate_tech_domains()
        
        # 如果LLM没有返回有效的域
        if not domains:
            raise Exception("Failed to generate tech domains")
        
        # 保存生成的域到数据库
        created_domains = []
        existing_domains = db_service.get_all_tech_domains()
        for domain in domains:
            try:
                # 检查是否已存在同名
                existing_names = {d.name for d in existing_domains}
                
                if domain["name"] not in existing_names:
                    # 实际保存到数据库
                    created_domain = db_service.create_tech_domain(name=domain["name"])
                    created_domains.append(created_domain)
            except Exception as e:
                print(f"Error creating domain {domain['name']}: {e}")
                continue
        
        # merge created_domains and existing_domains
        all_domains = list(set(created_domains + existing_domains))

        # 转换格式为前端需要的结构
        saved_domains = [
            {"name": d.name,} for d in all_domains
        ]
        
        return {"domains": saved_domains}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate tech domains: {str(e)}")

@router.get("/tech-domains", response_model=TechDomainsListResponse)
async def get_all_tech_domains():
    """
    Get all saved tech domains from database
    """
    try:
        domains = db_service.get_all_tech_domains()
        return {
            "domains": [
                {
                    "name": domain.name,
                }
                for domain in domains
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tech domains: {str(e)}")


@router.post("/tech-domains/delete", response_model=TechDomainDeleteResponse)
async def delete_tech_domain(request: TechDomainDeleteRequest):
    """
    Delete a specific tech domain from database
    使用 POST 请求以避免 URL 路径中特殊字符（如 "/"）的问题
    """
    try:
        success = db_service.delete_tech_domain(request.name)
        if success:
            return {"message": "Tech domain deleted successfully", "status": "success", "name": request.name}
        else:
            raise HTTPException(status_code=404, detail="Tech domain not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete tech domain: {str(e)}")

@router.post("/tech-domains/manual", response_model=TechDomainCreateResponse)
async def create_tech_domain_manual(request: TechDomainCreateRequest):
    """
    Manually create a single tech domain
    """
    try:
        created_domain = db_service.create_tech_domain(name=request.name.strip())
        return {
            "name": created_domain.name,
            "message": "Tech domain created successfully"
        }
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail="Tech domain already exists")
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tech domain: {str(e)}")

######################################### Tech Domain Question ########################################

# Question related models
class QuestionGenerateRequest(BaseModel):
    domain_name: str

class QuestionGetAllRequest(BaseModel):
    domain_name: str

class QuestionDeleteRequest(BaseModel):
    question_id: int

class QuestionDeleteAllRequest(BaseModel):
    domain_name: str

class QuestionManualCreateRequest(BaseModel):
    domain_name: str
    question_text: str
    generated_answer: Optional[str] = None

class QuestionResponse(BaseModel):
    id: int
    domain_name: str
    question_text: str
    user_answer: Optional[str] = None
    generated_answer: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class QuestionsListResponse(BaseModel):
    questions: List[QuestionResponse]

class QuestionCreateResponse(BaseModel):
    id: int
    domain_name: str
    question_text: str
    message: str

class QuestionDeleteResponse(BaseModel):
    message: str
    status: str
    question_id: int

class QuestionsDeleteAllResponse(BaseModel):
    message: str
    status: str
    domain_name: str
    deleted_count: int


@router.post("/tech-domains/questions/generate", response_model=QuestionsListResponse)
async def generate_tech_domain_questions(request: QuestionGenerateRequest):
    """
    Generate questions for a specific tech domain using LLM
    """
    try:
        # 先删除该领域的所有现有问题（重新生成时清空旧数据）
        deleted_count = question_db_service.delete_questions_by_domain(request.domain_name)
        if deleted_count > 0:
            print(f"Deleted {deleted_count} existing questions for domain: {request.domain_name}")

        # 使用真实的 LLM 服务生成问题
        questions_data = tech_question_service.generate_questions(request.domain_name)

        # 保存生成的问题到数据库
        created_questions = []
        for question_data in questions_data:
            try:
                # 使用真实的数据库服务创建问题
                created_question = question_db_service.create_question(
                    domain_name=request.domain_name,
                    question_text=question_data["question_text"],
                    generated_answer=question_data["generated_answer"]  # 现在是 None
                )

                # 转换为响应格式
                question_response = {
                    "id": created_question.id,
                    "domain_name": created_question.domain_name,
                    "question_text": created_question.question_text,
                    "user_answer": created_question.user_answer,
                    "generated_answer": created_question.generated_answer,
                    "created_at": str(created_question.created_at) if created_question.created_at else None,
                    "updated_at": str(created_question.updated_at) if created_question.updated_at else None
                }
                created_questions.append(question_response)
            except Exception as e:
                print(f"Error creating question: {e}")
                continue

        return {"questions": created_questions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")


@router.post("/tech-domains/questions/agentic_generate", response_model=QuestionsListResponse)
async def generate_tech_domain_questions_agentic(request: QuestionGenerateRequest):
    """
    使用 CrewAI 生成特定技术领域的面试题库
    """
    try:
        # 先删除该领域的所有现有问题
        deleted_count = question_db_service.delete_questions_by_domain(request.domain_name)
        if deleted_count > 0:
            print(f"Deleted {deleted_count} existing questions for domain: {request.domain_name}")

        # 使用 CrewAI 生成问题
        coordinator = CrewCoordinator()
        result = await coordinator.execute_question_generation_crew(request.domain_name)

        if result["status"] != "success":
            raise HTTPException(status_code=500, detail=f"CrewAI execution failed: {result.get('error', 'Unknown error')}")

        # 解析 CrewAI 的结果
        crew_result = result["result"]

        # 从最后一个任务的输出中提取问题
        if hasattr(crew_result, 'tasks_output') and crew_result.tasks_output:
            last_task_output = crew_result.tasks_output[-1]
            questions_json = last_task_output.raw if hasattr(last_task_output, 'raw') else str(last_task_output)
        else:
            questions_json = str(crew_result)

        # 解析 JSON 格式的问题
        import json
        try:
            questions_data = json.loads(questions_json)
            questions_list = questions_data.get("questions", [])
        except json.JSONDecodeError:
            # 如果不是 JSON 格式，尝试简单解析
            questions_list = [q.strip() for q in questions_json.split('\n') if q.strip()]

        # 保存生成的问题到数据库
        created_questions = []
        for question_text in questions_list:
            if question_text:
                try:
                    created_question = question_db_service.create_question(
                        domain_name=request.domain_name,
                        question_text=question_text,
                        generated_answer=None
                    )

                    question_response = {
                        "id": created_question.id,
                        "domain_name": created_question.domain_name,
                        "question_text": created_question.question_text,
                        "user_answer": created_question.user_answer,
                        "generated_answer": created_question.generated_answer,
                        "created_at": str(created_question.created_at) if created_question.created_at else None,
                        "updated_at": str(created_question.updated_at) if created_question.updated_at else None
                    }
                    created_questions.append(question_response)
                except Exception as e:
                    print(f"Error creating question: {e}")
                    continue

        return {"questions": created_questions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate questions with CrewAI: {str(e)}")


@router.post("/tech-domains/questions/get_all", response_model=QuestionsListResponse)
async def get_all_tech_domain_questions(request: QuestionGetAllRequest):
    """
    Get all questions for a specific tech domain
    """
    try:
        # 使用真实的数据库查询获取问题
        questions = question_db_service.get_questions_by_domain(request.domain_name)

        # 转换为响应格式
        questions_response = []
        for question in questions:
            question_data = {
                "id": question.id,
                "domain_name": question.domain_name,
                "question_text": question.question_text,
                "user_answer": question.user_answer,
                "generated_answer": question.generated_answer,
                "created_at": str(question.created_at) if question.created_at else None,
                "updated_at": str(question.updated_at) if question.updated_at else None
            }
            questions_response.append(question_data)

        return {"questions": questions_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get questions: {str(e)}")


@router.post("/tech-domains/questions/delete", response_model=QuestionDeleteResponse)
async def delete_tech_domain_question(request: QuestionDeleteRequest):
    """
    Delete a specific question by ID
    """
    try:
        # 使用真实的数据库操作删除问题
        success = question_db_service.delete_question(request.question_id)

        if success:
            return {
                "message": "Question deleted successfully",
                "status": "success",
                "question_id": request.question_id
            }
        else:
            raise HTTPException(status_code=404, detail="Question not found")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete question: {str(e)}")


@router.post("/tech-domains/questions/delete_all", response_model=QuestionsDeleteAllResponse)
async def delete_all_tech_domain_questions(request: QuestionDeleteAllRequest):
    """
    Delete all questions for a specific tech domain
    """
    try:
        # 使用真实的数据库操作删除所有问题
        deleted_count = question_db_service.delete_questions_by_domain(request.domain_name)

        return {
            "message": f"All questions for domain '{request.domain_name}' deleted successfully",
            "status": "success",
            "domain_name": request.domain_name,
            "deleted_count": deleted_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete all questions: {str(e)}")


@router.post("/tech-domains/questions/manual", response_model=QuestionCreateResponse)
async def create_tech_domain_question_manual(request: QuestionManualCreateRequest):
    """
    Manually create a question for a specific tech domain
    """
    try:
        # 使用真实的数据库操作创建问题
        created_question = question_db_service.create_question(
            domain_name=request.domain_name,
            question_text=request.question_text,
        )

        return {
            "id": created_question.id,
            "domain_name": created_question.domain_name,
            "question_text": created_question.question_text,
            "message": "Question created successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")
