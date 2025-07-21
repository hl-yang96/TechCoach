"""
CrewAI 框架测试

基础的单元测试和集成测试。
"""

import unittest
from unittest.mock import Mock, patch
from typing import Dict, Any

from .agent_manager import AgentManager
from .task_manager import TaskManager
from .crew_coordinator import CrewCoordinator
from .config import AgentConfig, TaskConfig, CrewConfig, AgentRole, TaskType


class TestAgentManager(unittest.TestCase):
    """Agent 管理器测试"""
    
    def setUp(self):
        self.agent_manager = AgentManager()
    
    def test_create_agent(self):
        """测试创建 Agent"""
        config = AgentConfig(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory"
        )
        
        with patch('app.agentic_core.crew.agent_manager.Agent') as mock_agent:
            mock_agent.return_value = Mock()
            agent = self.agent_manager.create_agent(config)
            
            self.assertIsNotNone(agent)
            self.assertIn("test_agent", self.agent_manager.agents)
    
    def test_create_agent_from_role(self):
        """测试从预定义角色创建 Agent"""
        with patch('app.agentic_core.crew.agent_manager.Agent') as mock_agent:
            mock_agent.return_value = Mock()
            agent = self.agent_manager.create_agent_from_role(AgentRole.RESEARCHER)
            
            self.assertIsNotNone(agent)
    
    def test_get_agent(self):
        """测试获取 Agent"""
        config = AgentConfig(
            role="Test Agent",
            goal="Test goal", 
            backstory="Test backstory"
        )
        
        with patch('app.agentic_core.crew.agent_manager.Agent') as mock_agent:
            mock_agent.return_value = Mock()
            self.agent_manager.create_agent(config)
            
            agent = self.agent_manager.get_agent("test_agent")
            self.assertIsNotNone(agent)
            
            non_existent = self.agent_manager.get_agent("non_existent")
            self.assertIsNone(non_existent)
    
    def test_list_agents(self):
        """测试列出所有 Agent"""
        self.assertEqual(len(self.agent_manager.list_agents()), 0)
        
        config = AgentConfig(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory"
        )
        
        with patch('app.agentic_core.crew.agent_manager.Agent') as mock_agent:
            mock_agent.return_value = Mock()
            self.agent_manager.create_agent(config)
            
            agents = self.agent_manager.list_agents()
            self.assertEqual(len(agents), 1)
            self.assertIn("test_agent", agents)


class TestTaskManager(unittest.TestCase):
    """Task 管理器测试"""
    
    def setUp(self):
        self.task_manager = TaskManager()
        self.mock_agent = Mock()
    
    def test_create_task(self):
        """测试创建 Task"""
        config = TaskConfig(
            description="Test task description",
            expected_output="Test output",
            agent_role="test_agent"
        )
        
        with patch('app.agentic_core.crew.task_manager.Task') as mock_task:
            mock_task.return_value = Mock()
            task = self.task_manager.create_task(config, self.mock_agent)
            
            self.assertIsNotNone(task)
            self.assertTrue(len(self.task_manager.tasks) > 0)
    
    def test_create_task_from_type(self):
        """测试从预定义类型创建 Task"""
        with patch('app.agentic_core.crew.task_manager.Task') as mock_task:
            mock_task.return_value = Mock()
            task = self.task_manager.create_task_from_type(
                TaskType.RESEARCH, 
                self.mock_agent,
                topic="AI"
            )
            
            self.assertIsNotNone(task)
    
    def test_get_task_dependencies(self):
        """测试获取任务依赖"""
        config = TaskConfig(
            description="Test task",
            expected_output="Test output",
            agent_role="test_agent"
        )
        
        with patch('app.agentic_core.crew.task_manager.Task') as mock_task:
            mock_task.return_value = Mock()
            task = self.task_manager.create_task(config, self.mock_agent)
            
            task_key = list(self.task_manager.tasks.keys())[0]
            dependencies = self.task_manager.get_task_dependencies(task_key)
            self.assertEqual(len(dependencies), 0)


class TestCrewCoordinator(unittest.TestCase):
    """Crew 协调器测试"""
    
    def setUp(self):
        self.coordinator = CrewCoordinator()
    
    def test_create_simple_crew(self):
        """测试创建简单 Crew"""
        with patch('app.agentic_core.crew.crew_coordinator.Crew') as mock_crew:
            with patch('app.agentic_core.crew.agent_manager.Agent') as mock_agent:
                with patch('app.agentic_core.crew.task_manager.Task') as mock_task:
                    mock_crew.return_value = Mock()
                    mock_agent.return_value = Mock()
                    mock_task.return_value = Mock()
                    
                    crew = self.coordinator.create_simple_crew(
                        name="Test Crew",
                        description="Test description",
                        agent_roles=["Researcher"],
                        task_descriptions=["Research task"]
                    )
                    
                    self.assertIsNotNone(crew)
                    self.assertIn("test_crew", self.coordinator.crews)
    
    def test_get_crew_info(self):
        """测试获取 Crew 信息"""
        with patch('app.agentic_core.crew.crew_coordinator.Crew') as mock_crew:
            with patch('app.agentic_core.crew.agent_manager.Agent') as mock_agent:
                with patch('app.agentic_core.crew.task_manager.Task') as mock_task:
                    mock_crew.return_value = Mock()
                    mock_agent.return_value = Mock()
                    mock_task.return_value = Mock()
                    
                    self.coordinator.create_simple_crew(
                        name="Test Crew",
                        description="Test description", 
                        agent_roles=["Researcher"],
                        task_descriptions=["Research task"]
                    )
                    
                    info = self.coordinator.get_crew_info("test_crew")
                    self.assertIsNotNone(info)
                    self.assertEqual(info["name"], "Test Crew")


class TestConfig(unittest.TestCase):
    """配置类测试"""
    
    def test_agent_config(self):
        """测试 Agent 配置"""
        config = AgentConfig(
            role="Test Role",
            goal="Test Goal",
            backstory="Test Backstory"
        )
        
        self.assertEqual(config.role, "Test Role")
        self.assertEqual(config.goal, "Test Goal")
        self.assertEqual(config.backstory, "Test Backstory")
        self.assertTrue(config.verbose)
        self.assertFalse(config.allow_delegation)
    
    def test_task_config(self):
        """测试 Task 配置"""
        config = TaskConfig(
            description="Test Description",
            expected_output="Test Output",
            agent_role="test_agent"
        )
        
        self.assertEqual(config.description, "Test Description")
        self.assertEqual(config.expected_output, "Test Output")
        self.assertEqual(config.agent_role, "test_agent")
    
    def test_crew_config(self):
        """测试 Crew 配置"""
        config = CrewConfig(
            name="Test Crew",
            description="Test Description"
        )
        
        self.assertEqual(config.name, "Test Crew")
        self.assertEqual(config.description, "Test Description")
        self.assertEqual(len(config.agents), 0)
        self.assertEqual(len(config.tasks), 0)
        
        # 测试添加 Agent
        agent_config = AgentConfig(
            role="Test Agent",
            goal="Test Goal",
            backstory="Test Backstory"
        )
        config.add_agent(agent_config)
        self.assertEqual(len(config.agents), 1)
        
        # 测试添加 Task
        task_config = TaskConfig(
            description="Test Task",
            expected_output="Test Output",
            agent_role="test_agent"
        )
        config.add_task(task_config)
        self.assertEqual(len(config.tasks), 1)


def run_tests():
    """运行所有测试"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
