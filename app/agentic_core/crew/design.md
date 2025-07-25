# 设计文档
## 概述

基于 CrewAI 进行 Agentic 的设计，从下至上为 Tools(工具) -> Agent(智能体) -> Task(任务)

## 需求分析
需求一：面试题生成
- 人类如何解决这个问题：
    - 首先看看我作为求职者的背景：工作经验，工作年限，求职目标
    - 然后去搜集各种资料：
        - 首先是关于某个技术领域(如操作系统)，需要对哪些大块的知识进行复习，给出一个大纲；
        - 然后再去搜索具体的面试题，无论是从面试经验贴，或者网上发布的题库；
    - 接下来，按照知识大纲的每一块甚至每一个小的知识点，去生成一些面试题目；
    - 最后，总结成一份题库文档，以大纲进行分类；


## 核心组件定义: Tools

作用: 
- 工具是智能体可以用来与外部世界交互或执行特定功能的函数。例如，搜索网络、读写文件、调用 API 等。
设计原则:
- 功能单一: 每个工具只做一件事，并把它做好；
- 描述清晰: 函数的文档字符串（docstring）应该清晰地描述工具的功能,CrewAI 会利用这个描述来判断何时使用该工具；
- 接口明确: 明确的参数和返回值，用于结构化调用和输出；

## 核心组件定义: Agent 角色

作用: 
- 执行任务的自治实体，有独特的角色描述、目标和背景故事，这些设定会指导其行动和决策。
- Tool 是绑定在 agent 上面的，每个 agent 有一系列工具可以用。

设计原则:
- 角色明确: role 应清晰定义其身份;
- 目标导向: goal 应具体说明其需要达成的最终目的;
- 背景故事: backstory 为智能体提供上下文和个性，影响其沟通风格和行为模式;
    ```
    role="Tech Content Strategist", 
    goal="Craft compelling content on tech advancements",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles. You transform complex concepts into compelling narratives.""",
    tools=["write_tool"]
    ```

### Task 设计
- 求职者背景分析                                   tools=[RAG]   
- 面试题大纲           dep-求职者背景分析            tools=[N]
- 面试题生成           dep-大纲\求职者背景分析        tools=[N]
- 面试题修正与补充      dep-面试题生成\求职者背景分析   tools=[RAG]
- 面试题汇总           dep-面试题修正与补充           tools=[N]

## 核心组件定义: Crew

作用: 
- Crew 是管理一系列 task 的一个流程的概念 (我感觉叫团队好像不太合理)，它负责编排任务的执行流程；
- Crew 可以配置一系列 task，然后可以通过 context 指定某个任务作为另一个任务的输入，从而实现任务的编排；
- 当然一个任务也可以运行，这个跟之前想的有点像，也是传统的 Agentic 的一种方式。但是 Crew 提供的 多任务 + 多Agent 的效果可能更好。