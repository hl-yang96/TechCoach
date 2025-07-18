# **Agentic AI 学习与面试教练：项目执行书**

### **Part 1: 项目蓝图与战略分析**

本部分旨在为项目奠定战略基础，确保每一项技术决策都与核心目标紧密对齐。作为一个技术精湛的独立开发者，您的目标不仅仅是构建一个工具，更是打造一个能够增强个人技术品牌、加速职业发展的战略性资产。

#### **1.1 项目愿景与核心价值定位**

在深入技术细节之前，必须明确项目的核心愿景。此项目不应被简单定义为一个“面试教练”，而应被定位为一个\*\*“个性化职业生涯领航员 (Personalized Career Co-pilot)”\*\*。这个定位将其从一个一次性工具提升为一个开发者职业生涯中的持续伙伴，能够陪伴用户从深度理解过往项目，到精准准备未来职位。

* **独特销售主张 (Unique Selling Proposition, USP):** 项目的核心差异化优势在于**通过 Agentic RAG 实现的超个性化**。与市面上依赖通用知识库的工具不同，本领航员将拥有一个关于*您个人*的深度、可检索的上下文知识库，涵盖您的代码、项目文档、职业目标乃至面试反馈。它不是一个通用的教练，而是您的专属技术参谋。  
* **核心用户旅程 (Target User Journey):** 设想一个典型的用户场景：一位准备更换工作的开发者。  
  1. **知识注入:** 用户首先将自己的整个职业历史“喂”给系统，包括连接其 GitHub 仓库、上传历史简历、项目设计文档和过去的绩效评估。  
  2. **目标对齐:** 用户输入一个或多个目标岗位的职位描述 (Job Description, JD)。  
  3. **智能分析与生成:** 系统利用其 Agentic 能力，分析 JD，并与用户的知识库进行比对。随后，它能自动为简历生成针对该 JD 的项目经历亮点，并构建一个高度定制化的模拟面试题库。  
  4. **模拟与复盘:** 用户基于这个定制题库进行模拟面试。面试结束后，系统能提供深度复盘报告，指出其在技术阐述、项目理解等方面的优劣势。

#### **1.2 功能分解与用户故事**

为了将宏大的愿景转化为可执行的开发任务，我们将功能需求分解为一系列用户故事，这些故事将构成后续开发冲刺的基础。

* **史诗 1: 知识摄取与上下文构建 (Knowledge Ingestion & Context Building)**  
  * 作为用户，我能够连接一个 Git 仓库，以便系统分析我的代码实现和贡献。  
  * 作为用户，我能够上传多种格式的文档（如 PDF, Markdown,.txt），例如我的简历、项目计划和技术方案。  
  * 作为用户，我能够通过文本输入我的长期职业目标和近期求职方向。  
* **史诗 2: 项目分析与摘要 (Project Analysis & Summarization)**  
  * 作为用户，我能够选择一个已摄取的项目，让 AI 自动生成关于该项目核心功能、技术栈以及我在其中贡献的简洁摘要。  
  * 作为用户，我能够让 AI 基于特定项目的代码和文档，为我的简历自动生成量化的、有影响力的成就描述点（bullet points）。  
* **史诗 3: “八股文”学习模块 (Interview Prep Module)**
  * 作为用户，我能够指定一个学习主题（例如，“Golang 并发模型”、“分布式系统设计”），让 AI 为我生成一个全面且结构化的题库。  
  * 作为用户，我能够要求 AI 将生成的题库与我已有的项目经历相结合，进行个性化定制，提出“在你的XX项目中，你是如何处理并发问题的？”这类问题。  
  * 作为用户，我能够进入“学习模式”，在该模式下我可以查看问题并选择性地显示或隐藏 AI 生成的标准答案。  
  * 作为用户，我能够进入“评分模式”，在该模式下我针对问题提供文本答案，AI 会根据预设的评分标准（rubric）给出分数和改进建议。  
* **史诗 4: 模拟面试与复盘 (Mock Interview Simulation)**  
  * 作为用户，我能够上传一个目标岗位的 JD，并启动一场完全基于此 JD 的模拟面试。  
  * 作为用户，我能够从我已生成的题库中随机抽取题目，进行一场综合性的模拟面试。  
  * 作为用户，我能够上传真实面试的录音文件，系统能够将其转录为文字并进行分析。  
  * 作为用户，我能够在面试后收到一份复盘报告，该报告分析我在面试中的表现，指出内容上的亮点与不足，并就如何更好地把握面试节奏提出建议。  
* **史诗 5: 简历与职业文档优化 (Resume & Career Document Optimization)**  
  * 作为用户，我能够上传我的现有简历和一份目标 JD，系统会分析两者之间的差距，并生成一个优化后的简历版本。  
  * 作为用户，我能够要求系统根据不同的岗位方向，为我生成多个版本的简历，突出不同的技能和项目重点。

此项目的核心功能要求 AI 具备两种截然不同的操作模式。第一种是\*\*“图书管理员 (Librarian)”**模式，其核心是 RAG，任务是从知识库中精确、忠实地检索事实。这对应于“项目梳理”和“八股文学习”等功能，这些功能要求对原始材料（代码、文档）有极高的保真度。第二种是**“教练 (Coach)”\*\*模式，其核心是生成、评估和创造。这对应于“模拟面试”、“简历优化”和“面试复盘”等功能，这些任务要求 AI 能够生成新的、有见地的文本，并根据复杂的标准评估用户的输入。

这种二元性对系统架构设计提出了明确要求。系统必须能够智能地在这两种模式间切换。图书管理员模式需要一个高精度的检索管道，而教练模式则需要精心设计的提示工程（Prompt Engineering）和可能更强大（也更昂贵）的语言模型（LLM）来进行细致入微的评估。因此，在后续的架构设计中，一个能够根据任务类型动态选择 LLM 和提示链的**LLM 路由模块 (LLM Router)** 变得至关重要。它不仅是实现功能所必需的，也是平衡系统响应质量与运营成本的关键所在。

### **Part 2: 系统架构与设计：模块化单体**

本部分将详细阐述系统的“如何构建”。我们将设计一个对于独立开发者而言足够简单、易于构建和部署，同时又具备足够扩展性以适应未来发展的系统。

#### **2.1 架构模式选择：“可分布式”的模块化单体 (The "Distribu-Ready" Modular Monolith)**

作为独立开发者，微服务架构带来的运维开销是难以承受的，而传统的“大泥球”式单体应用则会随着功能增加而变得难以维护，最终扼杀迭代速度和未来的可能性 \[1\]。因此，**模块化单体 (Modular Monolith)** 架构是本项目最理想的折中方案 \[2, 3\]。

该架构的核心优势在于：

* **开发简单性 (Simplicity):** 单一代码库、单一构建流程和单一的部署单元（一个 Docker 容器）极大地降低了开发和运维的复杂度，让您能将精力聚焦于功能实现而非基础设施 \[1, 2\]。  
* **高性能 (Performance):** 模块间的通信是进程内调用，避免了微服务架构中的网络延迟和序列化开销。这对于需要多步骤推理的 Agentic 工作流尤其有利，可以显著提升响应速度 \[1\]。  
* **面向未来 (Future-Proofing):** 通过在单体应用内部强制实施清晰的模块边界和 API 驱动的通信，我们构建了一个“为分布式准备就绪”的系统。未来，当某个模块（例如，高并发的面试评分服务）需要独立扩展时，可以依据“绞杀者无花果模式 (Strangler Fig Pattern)”将其平滑地重构并剥离为微服务，而无需对整个系统进行颠覆性改造 \[2, 4\]。这完美地满足了您对未来云端扩展性的要求，同时又避免了初期阶段的过度工程化。

#### **2.2 核心系统组件**

系统将由以下几个逻辑上独立、物理上集中的模块组成，它们共同存在于一个应用进程中。

*(注：此为示意图，实际实现中将以代码目录结构和接口定义体现)*

* **WebApp Gateway (API 网关层):** 这是系统的唯一入口。采用 FastAPI 构建，负责处理所有外部 HTTP 请求、用户认证（未来扩展）、请求体验证和路由分发。  
* **Ingestion Module (数据摄取模块):** 负责处理所有用户数据的接入。它包含一系列数据连接器（如 Git Connector, PDF Connector），用于解析原始数据，将其进行分块（Chunking），并传递给 Agentic Core 进行下一步处理。  
* **Agentic Core Module (Agentic 核心模块):** 这是整个系统的大脑。它封装了所有与 AI 相关的核心逻辑。  
  * 与向量数据库进行交互，负责嵌入（Embedding）的生成、存储和检索（RAG）。  
  * 包含关键的 **LLM 路由模块 (LLM Router)**，用于动态选择最合适的 LLM API。  
  * 管理和编排 Agentic 框架（如 LlamaIndex, CrewAI）及其使用的工具（如网络搜索）。  
* **Interview Prep Module (面试准备模块):** 包含“八股文”学习功能的业务逻辑。它编排对 Agentic Core 的调用，以实现题库生成、答案评分和学习会话管理等功能。  
* **Career Docs Module (职业文档模块):** 包含简历分析与生成等功能的业务逻辑。它通过调用 Agentic Core 来执行简历与 JD 的比对、内容生成等任务。  
* **Shared Kernel (共享内核):** 这是一个小型的、中心化的内部库，包含所有模块共用的数据结构（如 User, Document, InterviewSession）、接口定义和常量。其目的是为了避免代码重复，并确保模块间通信的一致性。

#### **2.3 LLM 路由模块：灵活性与成本控制的关键**

为了满足您在中国和海外市场使用不同 LLM 服务商、并根据任务差异化使用模型以优化成本的需求，设计一个强大的 LLM 路由模块是架构的核心。

* **目的:** 动态地为每个到来的任务选择最合适、最具成本效益的 LLM API。  
* **设计:** 该路由器将是 Agentic Core 模块中的一个专用类，实现一个责任链模式，并集成多种路由策略。  
* **路由策略:**  
  1. **静态/规则路由 (Static/Rule-Based Routing):** 对于任务类型明确、无需智能判断的请求，使用硬编码的规则进行路由。例如，一个规则可以是 task: "transcribe\_audio" \-\> model\_provider: "openai-whisper"。这是最快、最经济的策略 \[5, 6\]。  
  2. **语义相似度路由 (Semantic Similarity Routing):** 对于更复杂的任务，此策略将用户的查询（或任务描述）进行嵌入，然后与一个预定义的“任务嵌入向量”列表进行相似度计算。例如，预定义“项目摘要”、“面试答案评估”、“简历与JD对比”等任务的嵌入。通过找到最相似的任务向量来决定路由，这个过程避免了为路由本身进行一次 LLM 调用，从而节省了成本和延迟 \[6, 7\]。  
  3. **LLM 分类器路由 (LLM-as-Classifier Routing):** 对于最模糊、最开放的用户请求，我们将使用一个小型、快速且廉价的 LLM（如 Claude 3 Haiku, GPT-4o-mini）作为分类器。它的唯一职责是理解用户意图，并决定应该由哪个更强大、更专业的模型来执行实际任务。例如，当用户输入“帮我准备一下明天的面试”时，分类器需要判断这应该路由到“JD分析+模拟面试”流程，还是“八股文复习”流程 \[6, 8, 9\]。  
* **配置:** 路由器的所有规则和模型信息（如不同厂商的 API 端点、密钥、模型名称、价格信息）将通过一个外部的 YAML 配置文件进行管理。这使得您可以在不修改任何代码的情况下，轻松切换或添加新的 LLM 服务。

#### **2.4 数据流与持久化策略**

* **用户上传的原始文件 (Docs, Code):** 原始文件将被临时存储在挂载到 Docker 容器的本地持久化卷上。  
* **向量嵌入与元数据 (Vector Embeddings & Metadata):** 所有被摄取和分块的数据，在经过嵌入模型处理后，生成的向量及相关的元数据（如来源文件、块索引等）将被存储在向量数据库中。这是系统的核心记忆库 \[10, 11\]。  
* **用户与会话数据 (User & Session Data):** 用户的基本信息（初期可简化）、面试历史、生成的题库、评分记录等结构化关系数据，将被存储在一个 SQLite 数据库文件中。SQLite 是一个轻量级的、基于文件的数据库，无需额外配置服务，非常适合单用户的本地应用，完全符合当前阶段追求简单、快速开发的目标。该数据库文件也将存放在 Docker 的持久化卷上。

选择模块化单体架构，本身就是一项支持您“通过开源项目提升技术领导力”目标的战略决策。一个结构清晰的模块化单体项目，其代码库集中，逻辑边界明确（例如 AgenticCore, InterviewPrepModule），这使得其他开发者更容易理解和上手 \[2\]。相比于复杂的分布式微服务系统，它为潜在的社区贡献者提供了更低的入门门槛。当您将此项目开源时，其架构本身就成为了一个展示您深思熟虑的技术决策和架构成熟度的范例。在项目的 README 文件中明确阐述选择此架构的理由，将使项目从一个单纯的应用升华为一个具有教学意义的架构实践案例，这对于建立个人品牌和融入创业圈子具有不可估量的价值 \[4\]。

### **Part 3: 技术栈深度剖析与选型依据**

在这一部分，我们将做出具体的技术选型，并为每一个选择提供基于您特定需求的详尽论证：独立开发者、快速迭代、AI 核心。

#### **3.1 后端框架：Python (FastAPI)**

尽管您对 Go 和 C++ 同样熟悉，但在当前的 AI/ML 领域，Python 的生态系统拥有无可争议的领导地位 \[12, 13\]。

* **为什么选择 FastAPI?**  
  * **AI 生态协同效应:** 几乎所有主流的 AI 框架，包括 LlamaIndex、LangChain、CrewAI 等，都是 Python 原生的。选择 Python 可以消除技术整合的摩擦，并让您能直接利用最庞大、最活跃的库和社区资源 \[12\]。  
  * **卓越的 I/O 性能:** 本应用的核心瓶颈在于 I/O 密集型操作（即等待外部 LLM API 的网络响应），而非 CPU 密集型计算。FastAPI 基于 asyncio 的异步特性，使其在此类场景下的性能表现足以媲美 Node.js 和 Go \[12, 14\]。Go 语言的原始计算性能优势在这里无法成为决定性因素。  
  * **极致的开发效率:** FastAPI 通过 Pydantic 实现自动的数据模型校验和序列化，并通过 OpenAPI 规范自动生成交互式的 API 文档。这些特性极大地缩短了 API 的开发和调试时间，对于分秒必争的独立开发者而言至关重要 \[12\]。  
  * **平滑的学习曲线:** 其现代化的 Python 语法简洁直观。对于已经熟悉 Python 的您来说，可以非常迅速地投入到高效的开发中。

#### **3.2 前端框架：Vue.js**

在前端框架的选择上，主要的竞争者是 React 和 Vue。尽管 React 拥有更大的市场份额和人才库，但对于追求开发速度和易用性的场景，Vue 常常是更受推荐的选择 \[15, 16\]。

* **为什么选择 Vue.js?**  
  * **快速原型开发:** Vue 被形象地比作“微波炉”，能让您快速启动并运行项目 \[17\]。其“开箱即用”的特性，以及官方提供的路由（Vue Router）和状态管理（Pinia）库，为独立开发者减少了技术选型和集成的决策疲劳 \[18\]。  
  * **更平缓的学习曲线:** 对于非 React 生态的开发者来说，Vue 基于 HTML 模板的语法通常比 React 的 JSX 更为直观和易于上手。这让您可以将更多精力集中在功能实现上，而不是学习框架的特定范式 \[15, 18\]。  
  * **完全胜任当前任务:** 本应用的 UI 核心是功能性和数据驱动的，而非一个极度复杂、需要精细管理的超大规模界面。Vue 完全有能力处理这种复杂度的应用，并且在中小型项目中表现出色 \[15, 18\]。

#### **3.3 Agentic AI 框架：混合式、优中选优的策略**

您关于选择“大而全”还是“组合工具”的提问非常关键。研究表明，不同的 Agentic 框架在不同领域各有专长。采用单一的“大而全”框架（例如，所有任务都用 LangChain）必然会导致在某些方面做出妥协。因此，我们将采纳一种混合策略，集各家之长。

* **推荐组合:**  
  * **LlamaIndex (用于 RAG):** LlamaIndex 是为 RAG（Retrieval-Augmented Generation）量身打造的框架。在数据摄取、索引构建和查询优化方面，它提供了比其他通用框架更强大、更专业的能力 \[19, 20, 21\]。我们将使用 LlamaIndex 来构建与您的文档和向量数据库交互的核心 RAG 管道。  
  * **CrewAI (用于结构化工作流):** 对于那些步骤明确、可预测的多 Agent 任务，例如“分析 JD \-\> 对比简历 \-\> 生成新简历要点”，CrewAI 基于角色的结构化协作模式是理想选择。相比于更开放、更偏向研究的 AutoGen，CrewAI 的设置更简单，对于定义清晰的流程也更直观 \[22, 23, 24\]。我们可以将 LlamaIndex 构建的 RAG 管道封装成一个 Tool，供 CrewAI 的 Agent 调用。  
  * **LangChain (作为“胶水”层，按需使用):** 虽然我们将 LlamaIndex 和 CrewAI 作为核心，但 LangChain 庞大的集成库和丰富的工具函数使其成为一个宝贵的“瑞士军刀”。当需要某个特定的、LlamaIndex 或 CrewAI 尚未良好支持的工具（例如某个冷门的 API 集成）时，我们可以从 LangChain 中引入该组件，而无需采用其整个编排框架 \[25\]。

#### **3.4 向量数据库：ChromaDB (用于本地部署)**

基于您的核心需求——本地 Docker 部署、易于使用、零成本——我们对 ChromaDB、Qdrant 和 Weaviate 进行了比较。

* **为什么选择 ChromaDB?**  
  * **简单至上:** Chroma 被一致认为是入门最快、最简单的向量数据库，尤其适合本地开发和快速原型验证。它甚至可以作为库直接在内存中运行，或通过简单的 pip install 安装 \[10, 26, 27, 28\]。  
  * **Docker 友好:** Chroma 提供了官方的、配置简单的 Docker 镜像，完美契合我们基于 Docker Compose 的架构 \[29, 30\]。  
  * **满足初期规模:** 您的项目在启动阶段的向量数量将远低于千万级别。Chroma 完全能够满足这一规模的需求，同时避免了像 Milvus 或 Weaviate 这类为海量数据和高并发生产环境设计的数据库所带来的运维复杂性 \[10, 26\]。  
  * **生态系统无缝集成:** Chroma 在 LlamaIndex 和 LangChain 中都拥有一流的、开箱即用的支持 \[27\]。

#### **技术选型对比表**

为了更直观地展示选型依据，以下提供关键技术的对比分析。

**表 3.3: Agentic AI 框架对比**

| 框架           | 主要用例                  | 易用性 | 灵活性 | 在本项目中的关键优势                                      | 推荐角色            |
| :------------- | :------------------------ | :----- | :----- | :-------------------------------------------------------- | :------------------ |
| **LlamaIndex** | RAG (数据索引与检索)      | 高     | 中     | 专为 RAG 优化，提供高效的数据摄取和查询管道 \[20, 21\]。  | **核心 RAG 引擎**   |
| **LangChain**  | 通用 LLM 应用编排         | 中     | 高     | 生态系统庞大，工具集最全，可作为补充 \[19, 25\]。         | **“胶水层”/工具库** |
| **CrewAI**     | 结构化多 Agent 协作       | 高     | 中     | 基于角色的工作流设计清晰，适合自动化已知流程 \[23, 24\]。 | **结构化任务编排**  |
| **AutoGen**    | 开放式多 Agent 研究与探索 | 低     | 极高   | 擅长解决未知问题，但配置复杂，不适合快速开发 \[23, 31\]。 | 不推荐用于初期      |

**表 3.4: 向量数据库对比 (本地部署)**

| 标准                       | ChromaDB                     | Qdrant                       | Weaviate                 | 推荐理由                                             |
| :------------------------- | :--------------------------- | :--------------------------- | :----------------------- | :--------------------------------------------------- |
| **本地/Docker 设置易用性** | 极高 (pip 或单行 docker)     | 高 (提供 Docker 镜像)        | 高 (提供 Docker 镜像)    | ChromaDB 在本地开发场景下的简易性无与伦比 \[28\]。   |
| **主要用例**               | 原型验证，中小型应用         | 需要高级元数据过滤的生产应用 | 模块化、可扩展的生产应用 | ChromaDB 的定位完美契合本项目的起步阶段 \[10, 26\]。 |
| **可扩展性**               | 中等，适合千万级以下         | 高，Rust 核心性能强劲        | 高，专为规模化设计       | 初期无需 Qdrant/Weaviate 的高扩展性，未来可迁移。    |
| **过滤能力**               | 基础元数据过滤               | 强大，支持复杂载荷过滤       | 强大，支持混合搜索       | 项目初期对复杂过滤需求不高，ChromaDB 已足够 \[27\]。 |
| **生态集成**               | 优秀 (LlamaIndex, LangChain) | 良好                         | 良好                     | 三者集成度都很好，但 ChromaDB 的集成体验最无缝。     |
| **许可/成本**              | Apache 2.0 (完全免费)        | Apache 2.0 (完全免费)        | Apache 2.0 (完全免费)    | 三者开源版本均为免费，但 ChromaDB 的运维成本最低。   |

我们所选择的这一套技术栈——FastAPI, Vue.js, LlamaIndex, ChromaDB——是一个精心设计的\*\*“速度栈 (Velocity Stack)”\*\*。对于一个独立开发者项目而言，最大的风险不是未来无法扩展，而是在初期由于各种阻力而无法快速启动和迭代，最终失去动力。此处的每一项技术决策，都是为了最大化地降低认知负荷和开发摩擦，让您能够将宝贵的时间和精力投入到构建应用的核心、独特的功能上，而非在复杂的基础设施或陡峭的学习曲线中挣扎。这套技术栈本身也是开源 AI 社区的主流选择，这意味着丰富的文档、活跃的社区支持以及未来吸引贡献者的可能性，这都将成为您项目的战略性资产。

### **Part 4: 详细实施与分阶段开发路线图**

本部分为项目的构建提供一个具体的、可操作的步骤计划。我们将采用敏捷的冲刺（Sprint）模式，每个阶段都有明确的目标。

#### **4.1 阶段 0 \- 项目脚手架与持续集成 (Sprint 0\)**

此阶段的目标是搭建一个可以工作的最小化开发环境，验证技术栈的可行性。

* **任务:**  
  1. 初始化 Git 仓库，并根据模块化单体的思想创建清晰的目录结构（例如，/app/gateway, /app/agentic\_core, /app/interview\_prep 等）。  
  2. 编写核心的 docker-compose.yml 文件，用于编排后端（FastAPI）、前端（Vue）和向量数据库（ChromaDB）三个容器。  
  3. 为 FastAPI 应用编写基础的 Dockerfile。  
  4. 在 FastAPI 中实现一个简单的 /health 健康检查端点，并在 Vue 应用中创建一个基础页面来调用此端点，以确认前后端和网络通信正常。  
  5. 设置一个基础的 CI 流程（例如，使用 GitHub Actions），当代码推送到 main 分支时，自动构建 Docker 镜像并推送到 Docker Hub。

#### **4.2 阶段 1 \- “八股文” MVP (Sprints 1-3)**

此阶段的目标是快速交付核心的“八股文”学习功能，让产品具备初步的可用性。

* **Sprint 1: 题库生成与存储**  
  * **功能:** 用户可以输入一个主题，后端生成相应的题库。  
  * **实现:**  
    * **前端:** 构建一个简单的输入框和按钮，用于提交主题。  
    * **后端:** 在 InterviewPrepModule 中实现业务逻辑，调用 AgenticCore。AgenticCore 使用一个简单的提示模板（Prompt Template）向 LLM API 发送请求，要求其生成一个关于指定主题的问答列表（以 JSON 格式返回）。  
    * **数据层:** 将返回的 JSON 题库解析并存储到 SQLite 数据库中。  
* **Sprint 2: 学习模式**  
  * **功能:** 用户可以浏览题库，并选择性地查看答案。  
  * **实现:**  
    * **前端:** 构建一个列表页面，展示从后端获取的题库问题。每个问题旁边有一个“显示/隐藏答案”的按钮。  
    * **后端:** 提供一个 API，根据题库 ID 返回所有问题。当用户请求答案时，后端实时调用 AgenticCore，将问题发送给 LLM 生成答案。这样做可以确保答案内容始终是“新鲜”的，并且可以利用最新的模型能力。  
* **Sprint 3: 文本评分模式**  
  * **功能:** 用户可以对问题进行文字作答，并获得 AI 的评分和反馈。  
  * **实现:**  
    * **前端:** 在问题下方提供一个文本输入区域供用户作答。  
    * **后端:** 实现评分逻辑。这需要精心设计一个评分提示（详见 5.4 节），该提示将问题、用户的答案和“理想答案”一同发送给 AgenticCore。LLM 将被要求根据一个预设的评分标准（如准确性、完整性、清晰度）进行打分，并返回一个包含分数、理由和改进建议的结构化 JSON 对象。

#### **4.3 阶段 2 \- Agentic 能力跃迁 (Sprints 4-6)**

此阶段的重点是构建系统的核心记忆能力——RAG 管道，并引入 Agentic 工具。

* **Sprint 4: 基础 RAG 管道**  
  * **功能:** 系统能够摄取、处理和检索用户上传的文档。  
  * **实现:**  
    * 在 IngestionModule 中实现文档上传功能（支持 PDF 和.txt）。  
    * 使用 LlamaIndex 构建完整的 RAG 管道：加载文档 \-\> 使用 SentenceSplitter 分块 \-\> 调用嵌入模型 API 生成向量 \-\> 将向量和元数据存入 ChromaDB \[11, 32, 33\]。  
    * 构建一个简单的内部搜索 API，输入一个查询，返回最相关的文档块，用于测试 RAG 管道的有效性。  
* **Sprint 5: Agentic 网络搜索**  
  * **功能:** 为 Agent 赋予实时访问互联网信息的能力。  
  * **实现:**  
    * 选择一个搜索工具（如 Tavily, DuckDuckGo Search API）并将其集成为 AgenticCore 中的一个 Tool \[25, 34, 35\]。  
    * 创建一个测试性的 Agent，该 Agent 能够接收一个问题，并决定是查询内部知识库（RAG）还是使用网络搜索工具来回答。这是实现 JD 分析和获取最新行业信息的关键一步。  
* **Sprint 6: 上下文感知的题库生成**  
  * **功能:** 升级“八股文”功能，使其能够生成与用户背景高度相关的问题。  
  * **实现:**  
    * 修改 Sprint 1 中的题库生成逻辑。现在，生成问题的提示中不仅包含主题，还包含从用户上传的文档中通过 RAG 管道检索出的相关上下文。例如，提示可以是：“请为‘分布式缓存’这个主题生成面试题，并结合以下项目背景提出 2-3 个定制化问题：\[从用户简历中检索到的项目描述\]”。

#### **4.4 阶段 3 \- 高级功能与产品化 (Sprints 7-9)**

此阶段将交付更复杂的 Agentic 工作流，并对产品进行打磨，为开源发布做准备。

* **Sprint 7: 简历优化**  
  * **功能:** 用户上传简历和 JD，系统生成优化后的简历。  
  * **实现:**  
    * 构建 UI，允许用户同时上传简历文件和粘贴 JD 文本。  
    * 在 CareerDocsModule 中使用 CrewAI 实现一个多 Agent 工作流：  
      * **研究员 Agent:** 使用网络搜索工具，获取关于目标公司和职位的背景信息。  
      * **分析师 Agent:** 使用 RAG 工具，深度阅读用户的简历和项目文档。  
      * **作家 Agent:** 综合研究员和分析师的信息，对比 JD 要求与用户背景，重写简历中的关键部分，使其与目标岗位完美对齐。  
* **Sprint 8: 音频面试复盘**  
  * **功能:** 用户上传面试录音，系统转录并提供反馈。  
  * **实现:**  
    * 在 FastAPI 中实现一个支持音频文件（如.mp3,.wav）上传的端点 \[36\]。  
    * 后端接收文件后，调用 OpenAI Whisper API（或其开源替代品）进行语音转文本 \[37\]。  
    * 将转录后的完整对话文本，输入到一个专门用于面试复盘的评估提示中，获取关于用户在整场面试中表现的综合反馈。  
* **Sprint 9: 项目摘要与最终打磨**  
  * **功能:** 实现项目自动摘要功能，并完善整个产品。  
  * **实现:**  
    * 实现项目分析功能，通过 RAG 从指定的项目文档/代码中提取上下文，然后让 LLM 生成项目摘要。  
    * 对整体 UI/UX 进行优化，增加必要的错误处理和用户引导。  
    * 编写全面的 README.md 和其他必要的文档，为项目的开源发布做好准备。

### **Part 5: 核心组件实施指南**

本部分为系统中技术最关键、最新颖的几个组件提供具体的“如何做”指南。

#### **5.1 本地向量数据库设置 (Docker Compose)**

为了在本地环境中运行 ChromaDB 并与 FastAPI 应用连接，需要在 docker-compose.yml 文件中进行如下配置。

* **docker-compose.yml 片段:**  
  version: '3.8'  
  services:  
    backend:  
      build:.  
      ports:  
        \- "8001:8001" \# FastAPI app port  
      volumes:  
        \-./app\_data:/app/data \# Persistent storage for SQLite and raw files  
      depends\_on:  
        \- chroma  
      environment:  
        \- CHROMA\_HOST=chroma

    chroma:  
      image: chromadb/chroma  
      ports:  
        \- "8000:8000"  
      volumes:  
        \- chroma\_data:/chroma \# Persistent volume for vector data  
      command: "uvicorn chromadb.app:app \--host 0.0.0.0 \--port 8000"

  volumes:  
    chroma\_data:

  * **解释:**  
    * 我们定义了 backend 和 chroma 两个服务。  
    * chroma 服务使用官方的 chromadb/chroma 镜像 \[29\]。  
    * 通过 volumes 定义了一个名为 chroma\_data 的持久化数据卷，并将其挂载到 Chroma 容器的 /chroma 目录。这确保了即使容器重启，向量数据也不会丢失 \[30\]。  
    * backend 服务依赖于 chroma 服务，并通过环境变量 CHROMA\_HOST=chroma 来访问 ChromaDB 服务。  
* Python 客户端连接代码:  
  在 FastAPI 应用的 AgenticCore 模块中，使用 HttpClient 连接到 Docker 中的 ChromaDB 服务。  
  import chromadb  
  import os

  \# The host is the service name defined in docker-compose.yml  
  CHROMA\_HOST \= os.getenv("CHROMA\_HOST", "localhost")

  \# Connect to ChromaDB running in Docker  
  chroma\_client \= chromadb.HttpClient(host=CHROMA\_HOST, port=8000)

  \# Verify connection  
  try:  
      chroma\_client.heartbeat()  
      print("Successfully connected to ChromaDB.")  
  except Exception as e:  
      print(f"Failed to connect to ChromaDB: {e}")

  这段代码展示了如何从后端应用连接到在 Docker Compose 网络中名为 chroma 的服务 \[29\]。

#### **5.2 核心 RAG 管道实施 (LlamaIndex)**

以下是使用 LlamaIndex 构建核心 RAG 流程的 Python 代码分步演练 \[11, 32\]。

from llama\_index.core import (  
    VectorStoreIndex,  
    SimpleDirectoryReader,  
    StorageContext,  
    Settings,  
)  
from llama\_index.core.node\_parser import SentenceSplitter  
from llama\_index.vector\_stores.chroma import ChromaVectorStore  
from llama\_index.embeddings.openai import OpenAIEmbedding  
from llama\_index.llms.openai import OpenAI  
import chromadb

\# 1\. Setup Models and Global Settings  
Settings.llm \= OpenAI(model="gpt-4o")  
Settings.embed\_model \= OpenAIEmbedding(model="text-embedding-3-small")  
Settings.node\_parser \= SentenceSplitter(chunk\_size=512, chunk\_overlap=20)

\# 2\. Loading: Load documents from a local directory  
\# This assumes you have placed your PDF/TXT files in a './user\_docs' directory  
try:  
    documents \= SimpleDirectoryReader("./user\_docs").load\_data()  
except Exception as e:  
    print(f"Error loading documents: {e}")  
    documents \=

if documents:  
    \# 3\. Storing: Setup ChromaDB client and storage context  
    db \= chromadb.HttpClient(host="chroma", port=8000)  
    chroma\_collection \= db.get\_or\_create\_collection("interview\_coach\_collection")  
    vector\_store \= ChromaVectorStore(chroma\_collection=chroma\_collection)  
    storage\_context \= StorageContext.from\_defaults(vector\_store=vector\_store)

    \# 4\. Indexing: Create the index (this handles chunking and embedding automatically)  
    \# This process will convert documents into nodes, generate embeddings, and store them.  
    index \= VectorStoreIndex.from\_documents(  
        documents, storage\_context=storage\_context  
    )  
    print("Indexing complete.")

    \# 5\. Querying: Create a query engine to interact with the data  
    query\_engine \= index.as\_query\_engine(similarity\_top\_k=3)

    \# 6\. Generation: Ask a question  
    response \= query\_engine.query("What was my main contribution in the 'Project Apollo'?")  
    print(response)

* **代码解释:**  
  * **Settings:** LlamaIndex 允许通过全局 Settings 对象配置模型和解析器，简化后续代码 \[38\]。  
  * **Loading:** 使用 SimpleDirectoryReader 方便地从文件夹加载所有支持的文档类型 \[11\]。  
  * **Storing:** 我们首先创建到 ChromaDB 的连接，然后创建一个 ChromaVectorStore 实例，并将其包裹在 StorageContext 中。这告诉 LlamaIndex 将索引数据持久化到我们指定的 ChromaDB 集合中。  
  * **Indexing:** VectorStoreIndex.from\_documents 是一条高级命令，它在内部完成了分块（根据 Settings.node\_parser）、调用嵌入模型生成向量、并将节点存入 vector\_store 的所有工作 \[33\]。  
  * **Querying & Generation:** as\_query\_engine 创建了一个可以回答问题的接口。当你调用 query() 方法时，它会自动完成查询嵌入、向量搜索、检索上下文、构建提示并调用 LLM 生成最终答案的整个流程 \[32\]。

#### **5.3 音频处理端点 (FastAPI & Whisper)**

为实现面试录音的分析功能，需要一个能接收音频文件并进行转录的 API 端点。对于 MVP 阶段，一个简单的文件上传接口是最高效的选择。

from fastapi import FastAPI, UploadFile, File, HTTPException  
import openai  
import os  
import tempfile

app \= FastAPI()  
openai.api\_key \= os.getenv("OPENAI\_API\_KEY")

@app.post("/transcribe-audio/")  
async def transcribe\_audio(file: UploadFile \= File(...)):  
    """  
    Accepts an audio file, saves it temporarily, transcribes it using OpenAI Whisper,  
    and returns the transcription text.  
    """  
    if not file.content\_type.startswith("audio/"):  
        raise HTTPException(status\_code=400, detail="Invalid file type. Please upload an audio file.")

    \# Save the uploaded file to a temporary file  
    \# Using a temporary file is safer and more robust than in-memory processing for large files  
    try:  
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')\[-1\]}") as tmp:  
            contents \= await file.read()  
            tmp.write(contents)  
            tmp\_path \= tmp.name

        \# Call the Whisper API for transcription  
        with open(tmp\_path, "rb") as audio\_file:  
            transcription \= openai.audio.transcriptions.create(  
                model="whisper-1",  
                file=audio\_file,  
                response\_format="text"  
            )

    except Exception as e:  
        raise HTTPException(status\_code=500, detail=f"An error occurred during transcription: {str(e)}")  
    finally:  
        \# Clean up the temporary file  
        if 'tmp\_path' in locals() and os.path.exists(tmp\_path):  
            os.remove(tmp\_path)

    return {"transcription": transcription}

* **代码解释:**  
  * 该端点使用 FastAPI 的 UploadFile 类型来接收文件 \[36\]。  
  * 为了处理可能较大的音频文件并与 Whisper API 的文件读取方式兼容，代码首先将上传的文件保存到一个临时文件中。  
  * 然后，它以二进制读取模式打开这个临时文件，并将其传递给 OpenAI 的 whisper-1 模型进行转录 \[37\]。  
  * try...finally 结构确保无论转录成功与否，临时文件最终都会被删除，避免占用磁盘空间。  
  * 虽然 WebSocket 可以实现实时流式转录，但其实现复杂度更高。对于“上传录音并复盘”这一异步场景，文件上传的方式完全足够，且开发成本低得多 \[36\]。

#### **5.4 核心任务的提示工程 (Prompt Engineering)**

高质量的提示是驱动 AI 教练表现的核心。以下是两个关键任务的提示模板，它们遵循了角色扮演、提供上下文、要求结构化输出（JSON）和给出明确指令的最佳实践 \[39, 40\]。

* **模板 1: 简历与 JD 对比分析**  
  {  
    "role": "system",  
    "content": "You are an expert career coach and a professional resume writer for senior software engineers in the tech industry. Your task is to analyze a candidate's resume against a specific job description and provide actionable feedback. Output your response ONLY in a valid JSON format."  
  },  
  {  
    "role": "user",  
    "content": """  
    Please analyze the following resume and job description.

    \*\*Job Description:\*\*  
    \---  
    {job\_description\_text}  
    \---

    \*\*Candidate's Resume:\*\*  
    \---  
    {resume\_text}  
    \---

    Based on your analysis, perform the following steps:  
    1\. Identify the top 5 most critical skills and qualifications mentioned in the job description.  
    2\. For each critical skill, find direct or indirect evidence from the resume. If no evidence is found, state that clearly.  
    3\. Suggest 3 to 5 new or rephrased resume bullet points that better highlight the candidate's alignment with the job description. These suggestions should be concrete and use action verbs.

    Return your entire output as a single JSON object with the following structure:  
    {  
      "gap\_analysis":,  
      "suggested\_bullets":  
    }  
    """  
  }

  这个提示通过清晰的指令和强制的 JSON 输出格式，将一个复杂的分析任务分解为机器可读的结构化数据，便于前端展示和后续处理 \[41, 42\]。  
* **模板 2: 面试答案评分**  
  {  
    "role": "system",  
    "content": "You are a strict but fair technical interviewer at a top-tier tech company. You are evaluating a candidate's answer to a behavioral or system design question. Your evaluation must be objective and based on the provided rubric. Output your response ONLY in a valid JSON format."  
  },  
  {  
    "role": "user",  
    "content": """  
    Please evaluate the candidate's answer based on the provided question and the ideal answer points.

    \*\*Interview Question:\*\*  
    "{interview\_question}"

    \*\*Ideal Answer Points (What a good answer should cover):\*\*  
    \- {ideal\_answer\_point\_1}  
    \- {ideal\_answer\_point\_2}  
    \-...

    \*\*Candidate's Answer:\*\*  
    "{candidate\_answer\_text}"

    \*\*Evaluation Rubric:\*\*  
    \- \*\*Clarity (1-5):\*\* How clear and well-structured was the answer?  
    \- \*\*Technical Accuracy (1-5):\*\* Was the technical information provided correct?  
    \- \*\*Completeness (1-5):\*\* Did the answer cover all the key aspects mentioned in the ideal answer points?

    Provide a score for each category in the rubric, a brief (1-2 sentences) rationale for each score, and one single, concrete suggestion for improvement.

    Return your entire output as a single JSON object with the following structure:  
    {  
      "scores": {  
        "clarity": { "score": \<number\>, "rationale": "..." },  
        "technical\_accuracy": { "score": \<number\>, "rationale": "..." },  
        "completeness": { "score": \<number\>, "rationale": "..." }  
      },  
      "overall\_feedback": "A brief summary of the candidate's performance on this question.",  
      "suggestion\_for\_improvement": "One specific, actionable piece of advice."  
    }  
    """  
  }

  这个提示利用 LLM 作为“裁判”的能力，通过提供明确的评分标准和理想答案，引导模型进行高质量、可复现的评估，而不是给出泛泛的评论 \[40, 43, 44\]。

### **Part 6: 战略性增长与成功建议**

本部分将超越技术本身，为如何利用此项目实现您的非技术性目标——建立技术领导力和拓展人脉网络——提供战略性建议。

#### **6.1 开源策略**

一个成功的开源项目不仅仅是公开代码，更是构建一个社区和品牌。

* **仓库质量:** 创建一个专业、友好的代码仓库是第一步。这包括：  
  * 一份详尽的 README.md，不仅要说明如何安装和运行，更要阐述项目的愿景、核心价值以及关键的架构决策（特别是为什么选择模块化单体）。  
  * 一份 CONTRIBUTING.md 文件，清晰地说明社区贡献的流程和规范。  
  * 使用 GitHub 的 Issue 和 Pull Request 模板，引导用户提交高质量的反馈和贡献。  
* **文档先行:** 高质量的文档与代码同等重要。建议使用 MkDocs 或 Docusaurus 等工具为项目创建一个独立的文档网站。网站内容应深入解释您在技术选型和架构设计上的思考过程，将其打造为其他开发者学习 Agentic AI 和现代软件架构的资源。  
* **社区参与:** 主动推广项目是吸引关注的关键。  
  * 在 Medium、知乎或个人博客上撰写系列文章，记录您的开发历程和技术思考。  
  * 在 LinkedIn、Twitter (X) 等专业社交网络上分享项目进展和里程碑。  
  * 在本地或线上的开发者社区、技术大会上进行分享，展示您的项目。

#### **6.2 建立技术领导力**

这个项目是您个人技术品牌的绝佳素材。通过分享您的构建过程，您可以将自己定位为该领域的思想领袖。

* **内容创作主题:**  
  1. **《为何我为我的 AI 副业项目选择了模块化单体架构》:** 深入探讨单体与微服务的权衡，以及模块化单体如何成为 AI 应用的理想选择。  
  2. **《用 LlamaIndex 和 CrewAI 构建混合式 Agentic 框架：一次实践》:** 分享您如何结合不同框架的优点来解决实际问题。  
  3. **《LLM 路由深度解析：如何平衡 AI 应用的成本与性能》:** 详细介绍您的 LLM Router 设计，分享不同路由策略的优劣。  
* 这些文章展示的不仅仅是代码，更是您解决复杂问题的思考框架和工程智慧，这正是技术领导力的核心体现。

#### **6.3 人脉网络与商业化路径**

一个高质量的开源项目是强大的社交货币，能为您打开意想不到的大门。

* **人脉网络:** 当您向 AI 领域的创始人、投资人或资深工程师介绍自己时，这个项目就是您最好的名片。它为您提供了一个具体、可信的切入点，让交流不再空泛。  
* **潜在的商业化路径:**  
  * **专业版 (Pro Version):** 未来可以将应用部署到云端，提供一个功能更强大、无需本地部署的 SaaS 版本，面向个人求职者甚至企业的人力资源部门（如用于员工内训或裁员后的再就业辅导）。  
  * **API 服务:** 核心的简历优化、面试评估等功能，可以封装成独立的 API 服务，按调用次数收费。  
  * 模块化单体架构使得这种转型更为平滑。您可以选择性地将最具有商业价值的模块（如 CareerDocsModule）优先剥离出来，进行独立的商业化运营和扩展。

通过遵循这份详尽的执行书，您不仅能够成功地构建一个功能强大的个人工具，更能将其打造为一个展示您技术深度、战略眼光和领导潜力的标志性项目，为您的职业生涯开启新的篇章。