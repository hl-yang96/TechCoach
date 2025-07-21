"""
CrewAI 使用示例

提供各种 CrewAI 使用场景的示例代码。
"""

import os
from typing import Dict, Any

from .crew_coordinator import CrewCoordinator
from .agent_manager import AgentManager
from .task_manager import TaskManager
from .config import CrewConfig, AgentConfig, TaskConfig, AgentRole, TaskType


def example_job_seeker_analysis_crew() -> Dict[str, Any]:
    """
    示例：创建一个求职者分析 Crew

    Returns:
        包含 Crew 和执行结果的字典
    """
    # 创建协调器
    coordinator = CrewCoordinator()

    # 获取专业 Agents
    agent_manager = coordinator.agent_manager
    job_seeker_analyst = agent_manager.get_job_seeker_analyst()
    interview_expert = agent_manager.get_interview_question_expert()
    industry_expert = agent_manager.get_industry_expert()

    if not job_seeker_analyst or not interview_expert or not industry_expert:
        return {
            "error": "Failed to get professional agents",
            "status": "error"
        }

    # 创建 Crew 配置
    crew_config = CrewConfig(
        name="Job Seeker Analysis Team",
        description="A specialized team for job seeker background analysis and interview preparation"
    )

    # 添加任务
    analysis_task = TaskConfig(
        description="Analyze the job seeker's background, including work experience, technical skills, career goals, and provide comprehensive insights",
        expected_output="A detailed analysis report of the job seeker's profile with strengths, weaknesses, and recommendations",
        agent_role="Job Seeker Background Analyst"
    )
    crew_config.add_task(analysis_task)

    interview_task = TaskConfig(
        description="Based on the job seeker analysis, generate a comprehensive set of interview questions tailored to their background and target positions",
        expected_output="A structured interview question bank with different difficulty levels and categories",
        agent_role="面试题库生成专家"
    )
    crew_config.add_task(interview_task)

    industry_task = TaskConfig(
        description="Provide comprehensive industry knowledge analysis, including technical trends, skill requirements, and career development insights for the job seeker's target field",
        expected_output="A detailed industry analysis report with knowledge framework and learning recommendations",
        agent_role="行业知识专家"
    )
    crew_config.add_task(industry_task)

    # 创建 Crew
    try:
        crew = coordinator.create_crew(crew_config)
        return {
            "crew": crew,
            "status": "success",
            "message": "Job seeker analysis crew created successfully"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }


def example_analysis_crew() -> Dict[str, Any]:
    """
    示例：创建一个数据分析 Crew
    
    Returns:
        包含 Crew 和执行结果的字典
    """
    coordinator = CrewCoordinator()
    
    # 使用预定义角色创建 Crew
    crew_config = CrewConfig(
        name="Analysis Team",
        description="A team specialized in data analysis and insights"
    )
    
    # 添加研究员
    researcher_config = AgentConfig(
        role="Data Researcher",
        goal="Gather and organize relevant data for analysis",
        backstory="You are an expert at finding and organizing data from various sources."
    )
    crew_config.add_agent(researcher_config)
    
    # 添加分析师
    analyst_config = AgentConfig(
        role="Data Analyst",
        goal="Analyze data and extract meaningful insights",
        backstory="You are a skilled data analyst with expertise in statistical analysis."
    )
    crew_config.add_agent(analyst_config)
    
    # 添加任务
    research_task = TaskConfig(
        description="Research and collect data about market trends in AI technology",
        expected_output="A comprehensive dataset with relevant market information",
        agent_role="Data Researcher"
    )
    crew_config.add_task(research_task)
    
    analysis_task = TaskConfig(
        description="Analyze the collected data and identify key trends and insights",
        expected_output="A detailed analysis report with key findings and recommendations",
        agent_role="Data Analyst"
    )
    crew_config.add_task(analysis_task)
    
    # 创建 Crew
    crew = coordinator.create_crew(crew_config)
    
    try:
        result = coordinator.execute_crew("analysis_team")
        return {
            "crew": crew,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "crew": crew,
            "error": str(e),
            "status": "error"
        }


def example_hierarchical_crew() -> Dict[str, Any]:
    """
    示例：创建一个层次化管理的 Crew
    
    Returns:
        包含 Crew 和执行结果的字典
    """
    coordinator = CrewCoordinator()
    
    crew_config = CrewConfig(
        name="Hierarchical Team",
        description="A hierarchically managed team for complex projects",
        process="hierarchical"
    )
    
    # 添加多个专业角色
    roles_and_goals = [
        ("Market Researcher", "Research market trends and opportunities"),
        ("Product Analyst", "Analyze product requirements and specifications"),
        ("Technical Writer", "Create technical documentation and reports"),
        ("Quality Reviewer", "Review and validate all outputs for quality")
    ]
    
    for role, goal in roles_and_goals:
        agent_config = AgentConfig(
            role=role,
            goal=goal,
            backstory=f"You are an expert {role.lower()} with years of experience."
        )
        crew_config.add_agent(agent_config)
    
    # 添加相关任务
    tasks = [
        ("Research the current market landscape for AI tools", "Market Researcher"),
        ("Analyze the technical requirements for a new AI product", "Product Analyst"),
        ("Write a comprehensive product specification document", "Technical Writer"),
        ("Review all documents for accuracy and completeness", "Quality Reviewer")
    ]
    
    for task_desc, agent_role in tasks:
        task_config = TaskConfig(
            description=task_desc,
            expected_output="A professional and detailed deliverable",
            agent_role=agent_role
        )
        crew_config.add_task(task_config)
    
    crew = coordinator.create_crew(crew_config)
    
    try:
        result = coordinator.execute_crew("hierarchical_team")
        return {
            "crew": crew,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "crew": crew,
            "error": str(e),
            "status": "error"
        }


def example_custom_tools_crew():
    """
    示例：创建带有自定义工具的 Crew
    
    注意：这个示例展示了如何集成工具，但需要实际的工具实现
    """
    coordinator = CrewCoordinator()
    
    # 这里可以添加自定义工具
    # custom_tools = [search_tool, analysis_tool, write_tool]
    
    crew_config = CrewConfig(
        name="Tool-Enhanced Team",
        description="A team with specialized tools for enhanced capabilities"
    )
    
    # 添加带工具的 Agent
    agent_config = AgentConfig(
        role="Enhanced Researcher",
        goal="Conduct research using advanced tools",
        backstory="You have access to powerful research and analysis tools.",
        tools=["search_tool", "analysis_tool"]  # 工具名称列表
    )
    crew_config.add_agent(agent_config)
    
    task_config = TaskConfig(
        description="Research and analyze the latest developments in machine learning",
        expected_output="A comprehensive research report with data analysis",
        agent_role="Enhanced Researcher",
        tools=["search_tool", "analysis_tool"]
    )
    crew_config.add_task(task_config)
    
    return coordinator.create_crew(crew_config)


def run_all_examples():
    """运行所有示例"""
    print("=== CrewAI Framework Examples ===\n")
    
    examples = [
        ("Research Crew", example_research_crew),
        ("Analysis Crew", example_analysis_crew),
        ("Hierarchical Crew", example_hierarchical_crew)
    ]
    
    results = {}
    
    for name, example_func in examples:
        print(f"Running {name} example...")
        try:
            result = example_func()
            results[name] = result
            print(f"✓ {name} completed successfully")
        except Exception as e:
            results[name] = {"error": str(e), "status": "error"}
            print(f"✗ {name} failed: {str(e)}")
        print()
    
    return results


if __name__ == "__main__":
    # 运行示例（需要设置适当的环境变量）
    if os.getenv("OPENAI_API_KEY"):
        run_all_examples()
    else:
        print("Please set OPENAI_API_KEY environment variable to run examples.")
