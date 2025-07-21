"""
专业 Agents 测试脚本

测试新的求职者背景分析师和面试题生成专家 Agents。
"""

import logging
from typing import Dict, Any

from .agent_manager import AgentManager, PROFESSIONAL_AGENT_CONFIGS
from .task_manager import TaskManager, PROFESSIONAL_TASK_CONFIGS
from .crew_coordinator import CrewCoordinator
from .config import CrewConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_professional_agent_configs():
    """测试专业 Agent 配置"""
    print("=== 测试专业 Agent 配置 ===\n")

    for agent_type, config in PROFESSIONAL_AGENT_CONFIGS.items():
        print(f"Agent 类型: {agent_type}")
        print(f"角色: {config.role}")
        print(f"目标: {config.goal[:100]}...")
        print(f"背景: {config.backstory[:100]}...")
        print(f"工具: {config.tools}")
        print("-" * 50)


def test_professional_task_configs():
    """测试专业 Task 配置"""
    print("\n=== 测试专业 Task 配置 ===\n")

    for task_type, config in PROFESSIONAL_TASK_CONFIGS.items():
        print(f"Task 类型: {task_type}")
        print(f"描述: {config.description[:100]}...")
        print(f"期望输出: {config.expected_output[:100]}...")
        print(f"Agent 角色: {config.agent_role}")
        print("-" * 50)


def test_agent_manager_initialization():
    """测试 Agent 管理器初始化"""
    print("\n=== 测试 Agent 管理器初始化 ===\n")
    
    try:
        # 创建 Agent 管理器（不自动初始化）
        agent_manager = AgentManager(auto_initialize=False)
        print("✓ Agent 管理器创建成功")
        
        # 手动初始化专业 Agents
        success = agent_manager.initialize_professional_agents()
        if success:
            print("✓ 专业 Agents 初始化成功")
        else:
            print("✗ 专业 Agents 初始化失败")
            return False
        
        # 检查 Agents 是否创建成功
        agents = agent_manager.list_agents()
        print(f"创建的 Agents: {agents}")
        
        # 测试获取专业 Agents
        job_analyst = agent_manager.get_job_seeker_analyst()
        interview_expert = agent_manager.get_interview_question_expert()
        industry_expert = agent_manager.get_industry_expert()

        if job_analyst:
            print("✓ 求职者背景分析师获取成功")
        else:
            print("✗ 求职者背景分析师获取失败")

        if interview_expert:
            print("✓ 面试题生成专家获取成功")
        else:
            print("✗ 面试题生成专家获取失败")

        if industry_expert:
            print("✓ 行业知识专家获取成功")
        else:
            print("✗ 行业知识专家获取失败")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False


def test_task_manager_initialization():
    """测试 Task 管理器初始化"""
    print("\n=== 测试 Task 管理器初始化 ===\n")

    try:
        # 创建 Task 管理器
        task_manager = TaskManager(auto_initialize=True)
        print("✓ Task 管理器创建成功")

        # 检查专业 task 配置
        task_types = task_manager.list_professional_task_types()
        print(f"专业 Task 类型: {task_types}")

        # 测试获取专业 task 配置
        for task_type in task_types:
            config = task_manager.get_professional_task_config(task_type)
            if config:
                print(f"✓ {task_type} 配置获取成功")
            else:
                print(f"✗ {task_type} 配置获取失败")

        # 测试获取 task 信息
        for task_type in task_types:
            info = task_manager.get_professional_task_info(task_type)
            if info:
                print(f"✓ {task_type} 信息获取成功")
            else:
                print(f"✗ {task_type} 信息获取失败")

        return True

    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False


def test_agent_info():
    """测试获取 Agent 信息"""
    print("\n=== 测试 Agent 信息获取 ===\n")
    
    try:
        agent_manager = AgentManager(auto_initialize=False)
        agent_manager.initialize_professional_agents()
        
        for agent_key in agent_manager.list_agents():
            info = agent_manager.get_agent_info(agent_key)
            if info:
                print(f"Agent: {agent_key}")
                print(f"  角色: {info['role']}")
                print(f"  目标: {info['goal'][:80]}...")
                print(f"  工具: {info['tools']}")
                print()
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False


def test_crew_creation():
    """测试 Crew 创建"""
    print("\n=== 测试 Crew 创建 ===\n")
    
    try:
        # 创建协调器
        coordinator = CrewCoordinator()
        
        # 检查专业 Agents 是否可用
        job_analyst = coordinator.agent_manager.get_job_seeker_analyst()
        interview_expert = coordinator.agent_manager.get_interview_question_expert()
        industry_expert = coordinator.agent_manager.get_industry_expert()

        if not job_analyst or not interview_expert or not industry_expert:
            print("✗ 专业 Agents 不可用")
            return False

        print("✓ 所有专业 Agents 可用")
        
        # 创建简单的 Crew 配置
        crew_config = CrewConfig(
            name="Test Professional Crew",
            description="Test crew with professional agents"
        )
        
        # 创建 Task 管理器并获取专业 task 配置
        task_manager = TaskManager()

        # 使用专业 task 配置
        analysis_config = task_manager.get_professional_task_config("job_seeker_analysis")
        knowledge_config = task_manager.get_professional_task_config("technical_knowledge_outline")
        interview_config = task_manager.get_professional_task_config("interview_question_bank")

        if not analysis_config or not knowledge_config or not interview_config:
            print("✗ 无法获取专业 task 配置")
            return False

        crew_config.add_task(analysis_config)
        crew_config.add_task(knowledge_config)
        crew_config.add_task(interview_config)
        
        # 创建 Crew
        crew = coordinator.create_crew(crew_config)
        if crew:
            print("✓ Crew 创建成功")
            
            # 获取 Crew 信息
            info = coordinator.get_crew_info("test_professional_crew")
            if info:
                print(f"Crew 信息: {info['name']}")
                print(f"Agents 数量: {info['agents_count']}")
                print(f"Tasks 数量: {info['tasks_count']}")
            
            return True
        else:
            print("✗ Crew 创建失败")
            return False
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("=== 专业 Agents 测试套件 ===\n")
    
    tests = [
        ("Agent 配置测试", test_professional_agent_configs),
        ("Task 配置测试", test_professional_task_configs),
        ("Agent 管理器初始化", test_agent_manager_initialization),
        ("Task 管理器初始化", test_task_manager_initialization),
        ("Agent 信息获取", test_agent_info),
        ("Crew 创建", test_crew_creation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results[test_name] = result
            status = "✓ 通过" if result else "✗ 失败"
            print(f"\n{test_name}: {status}")
        except Exception as e:
            results[test_name] = False
            print(f"\n{test_name}: ✗ 异常 - {str(e)}")
    
    # 总结
    print(f"\n{'='*50}")
    print("测试总结:")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {test_name}")
    
    return results


if __name__ == "__main__":
    run_all_tests()
