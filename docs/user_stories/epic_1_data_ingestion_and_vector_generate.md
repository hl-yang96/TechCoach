# 个人职业发展AI助手：分阶段资料集成

## 摘要

本报告旨在为“个人职业发展AI助手”项目，提供一个清晰、分阶段的数据集成路线图。该计划以“求职”为核心目标，通过两个阶段的资料整合，逐步将系统从一个高效的“求职材料处理器”升级为一个具备深度市场洞察和面试分析能力的“智能求职战略伙伴”。

## 知识库设计：面向Agentic RAG的ChromaDB集合构建

为了将上述分阶段的资料转化为一个能被AI Agent高效利用的知识库，我们需要精心设计ChromaDB的集合（Collection）结构。核心原则是：通过清晰的集合划分和丰富的元数据（Metadata），为Agent的思考和决策提供明确的线索。

---

## 第一阶段：构建核心求职档案 (Core Job-Seeking Profile)

此阶段的集合旨在为Agent提供关于“我”和“市场”的基础事实。

### 集合名称: `resumes`
- **描述 (Description):** "存储用户所有版本的个人简历。用于快速查找、匹配和定制简历以适应不同岗位。"
- **元数据 (Metadata/Tags):**
    - `target_job`: (字符串) 目标岗位方向，例如: "后端工程师", "项目经理"
    - `language`: (字符串) 简历语言，例如: "中文", "英文"
    - `last_updated`: (日期) "2025-07-20"

### 集合名称: `projects_experience`
- **描述 (Description):** "存储用户所有项目和工作经验的详细材料，作为简历内容的支撑和扩展。"
- **元数据 (Metadata/Tags):**
    - `project_name`: (字符串) 项目名称，例如: "XX电商平台支付系统"
    - `document_type`: (枚举) 文档类型，例如: "技术方案", "市场分析报告", "复盘总结"
    - `is_technical`: (布尔值) `true` / `false`
    - `related_resume_version`: (字符串) 关联的简历版本号，例如: "v2.1_backend_focused"

### 集合名称: `job_postings`
- **描述 (Description):** "存储收集到的目标岗位JD。用于市场需求分析、技能差距识别和简历匹配。"
- **元数据 (Metadata/Tags):**
    - `company_name`: (字符串) 公司名称，例如: "Google", "Startup Inc."
    - `job_title`: (字符串) 职位名称，例如: "高级软件工程师"
    - `source_url`: (字符串) 招聘信息来源链接

---

## 第二阶段：深化洞察与市场对齐 (Deepening Insights & Market Alignment)

此阶段的集合旨在为Agent提供更深层次的分析和预测能力。

### 集合名称: `interviews`
- **描述 (Description):** "存储所有面试的记录、问题和反馈。用于复盘、发现知识盲区和预测高频考点。"
- **元数据 (Metadata/Tags):**
    - `company_name`: (字符串) "Microsoft"
    - `job_title`: (字符串) "产品经理"
    - `interview_round`: (枚举) 面试轮次，例如: "HR面", "技术一面", "总监面"
    - `result`: (枚举) "通过", "未通过", "待定"
    - `interview_date`: (日期) "2025-08-15"

### 集合名称: `interview_qna_bank`
- **描述 (Description):** "从互联网、论坛、GitHub等渠道收集的通用面试题库，用于补充和扩展个人面试经验，进行模拟训练。"
- **元数据 (Metadata/Tags):**
    - `source`: (字符串) 来源，例如: "GitHub-awesome-interviews", "LeetCode"
    - `job_domain`: (字符串) 职位领域，例如: "后端", "前端", "数据科学"
    - `question_type`: (枚举) 问题类型，例如: "算法", "系统设计", "行为面试"

### 集合名称: `code_analysis`
- **描述 (Description):** "（针对开发者）存储对用户代码库的静态分析结果和摘要。用于客观评估技术能力和梳理技术亮点。"
- **元数据 (Metadata/Tags):**
    - `repo_name`: (字符串) "my-ai-project"
    - `primary_language`: (字符串) "Python"
    - `key_frameworks`: (列表) `["FastAPI", "Pydantic", "LlamaIndex"]`
    - `analysis_date`: (日期) "2025-09-01"

### 集合名称: `industry_trends`
- **描述 (Description):** "存储行业报告和技术趋势分析文章。用于提升对话的战略高度和行业视野。"
- **元数据 (Metadata/Tags):**
    - `report_source`: (字符串) 报告来源，例如: "Gartner", "InfoQ"
    - `publish_date`: (日期) "2025-06-30"
    - `key_topics`: (列表) `["AI Agent", "RAG", "Multi-modal"]`

---

## Agentic RAG如何利用此设计

一个设计良好的Agent，其思考链条会是：

1.  **理解意图:** 用户提问“帮我找一份适合投递谷歌AI岗位的简历”。
2.  **选择集合:** Agent通过理解集合的描述，判断出需要查询`resumes`和`job_postings`两个集合。
3.  **过滤与查询:**
    - 在`job_postings`中，使用元数据`company_name="Google"`和关键词“AI”进行查询，找到对应的JD。
    - 分析JD后，提取核心要求。
    - 在`resumes`中，使用元数据`target_job`进行初筛，再用JD的核心要求作为查询向量，找到最匹配的简历版本。
4.  **整合与回答:** 将找到的简历版本和分析结果呈现给用户。

这种设计将数据处理的复杂性前置到了数据库构建阶段，极大地降低了Agent在运行时的工作量，使其能更专注于“思考”和“决策”。