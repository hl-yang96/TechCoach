# TechCoach - AI-Powered Career Coaching Platform

Welcome to **TechCoach**, your personalized AI career coach that combines Retrieval Augmented Generation (RAG) with Agentic AI to provide customized interview preparation, resume optimization, and career guidance.

## Current Status
- Still in development
- Welcome for requests!

## 🎯 Project Overview

**TechCoach** is a **modular monolith** architecture designed for rapid development with future microservice extraction capability. This approach provides the simplicity of a monolith while maintaining clear module boundaries for scalability.

### Core Features
- **AI-Powered Interview Preparation** - Generate role-specific questions and get feedback
- **Resume Optimization** - Analyze and optimize resumes against job descriptions
- **Personalized Coaching** - Leverages RAG to incorporate your career history and projects
- **Multi-Format Document Processing** - Support for PDFs, Git repositories, Markdown, and more
- **LLM Router** - Intelligent model selection for cost-effectiveness and performance

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+ (for frontend development)

### Development Setup

1. **Environment Configuration**
   ```bash
   cp config/.env.template .env
   # Edit .env with your API keys and settings
   ```

2. **Using Docker Compose (Recommended)**
   ```bash
   # Build and start all services
   docker-compose up --build
   
   # Backend accessible at http://localhost:8001
   # Frontend accessible at http://localhost:3000
   ```

3. **Manual Development Setup**
   ```bash
   # Backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8001
   
   # Frontend
   cd frontend
   npm install
   npm run dev
   ```

### API Documentation
- **Swagger UI**: http://localhost:8001/docs
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## 🏗️ Architecture - "Distribu-Ready" Modular Monolith

### Module Structure
```
techcoach/
├── app/
│   ├── __init__.py                  # Main application package
│   ├── main.py                      # FastAPI entry point
│   ├── gateway/                     # API routing layer
│   │   ├── routers/                 # API endpoints
│   │   └── middleware/              # HTTP middleware
│   ├── agentic_core/                # AI orchestration
│   │   ├── rag/                     # LlamaIndex RAG pipeline
│   │   ├── llm_router/              # Dynamic LLM selection
│   │   └── tools/                   # AI integrations
│   ├── interview_prep/              # Interview system
│   │   └── service.py               # Interview logic
│   ├── career_docs/                 # Resume optimization
│   │   └── service.py               # Career document services
│   ├── ingestion/                   # Data ingestion
│   │   ├── connectors/              # Git, file system connectors
│   │   └── parsers/                 # Content parsers
│   └── shared_kernel/               # Common utilities
│       ├── models.py                # Type definitions
│       ├── constants.py             # Global constants
│       ├── exceptions.py            # Custom exceptions
│       └── validators.py            # Input validation
├── frontend/                        # Vue.js 3 application
├── tests/                          # Test suites
│   ├── integration/                 # End-to-end tests
│   └── unit/                        # Unit tests
├── config/                         # Configuration files
├── scripts/                        # Utility scripts
└── docker-compose.yml              # Container orchestration
```

### Key Architecture Features
- **Process-Level Boundaries**: Each module is isolated at the process level
- **Shared Kernel**: Common utilities and models to avoid duplication
- **Future-Ready**: Easy extraction to microservices via Strangler Fig pattern
- **Zero Downtime**: Background task processing for heavy operations

## 🔧 Development Commands

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Development server
uvicorn app.main:app --reload

# Testing
pytest tests/

# Linting
ruff check .
black .

# Type checking
mypy app/
```

### Frontend Development
```bash
cd frontend
npm install

# Development server
npm run dev

# Build for production
npm run build

# Test
npm run test
```

### Docker Commands
```bash
# Build and start
docker-compose up --build

# Rebuild specific service
docker-compose up --build backend

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Clean up volumes
docker-compose down -v
```

## 📊 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | FastAPI (Python) | High-performance ASGI web framework |
| **Frontend** | Vue.js 3 | Progressive JavaScript framework |
| **RAG Engine** | LlamaIndex | Advanced RAG and document processing |
| **Agents** | CrewAI | Multi-agent workflow orchestration |
| **Vector DB** | ChromaDB | Local vector database for embeddings |
| **Frameworks** | LangChain | LLM integrations and tools |
| **Data** | SQLite + Chroma | Hybrid storage approach |
| **Containerization** | Docker | Consistent deployment |

## 🔄 LLM Router Configuration

The LLM Router uses three strategies for model selection:

1. **Rule-based routing** (fastest) - Hard-coded task-to-model mappings
2. **Semantic similarity** - Vector-based task classification
3. **LLM classifier** - Small model for complex requests

Configuration: `config/llm_router.yaml`

Supported providers:
- **OpenAI**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Anthropic**: Claude 3.5 Sonnet, Claude 3.5 Haiku

## 🤖 AI Integration Patterns

### RAG Pipeline Flow
```
User Upload → Chunking → Embedding → ChromaDB → Retrieval → Context Injection → LLM Response
```

### Agent Patterns
- **Librarian Mode**: High-fidelity retrieval for project analysis
- **Coach Mode**: Generative and evaluative for interview prep

## 🔐 Environment Variables

Copy `config/.env.template` to `.env` and configure:

```bash
# Required
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here  # Optional

# Database
DATABASE_URL=sqlite:///app_data/techcoach.db

# Vector Database
CHROMA_HOST=chroma  # Docker service name
```

## 📈 Monitoring & Logging

- **API Health**: http://localhost:8001/health
- **Detailed Status**: http://localhost:8001/health/detailed
- **Logs directory**: ./logs/
- **Logging levels**: DEBUG, INFO, WARNING, ERROR

## 🧪 Testing Strategy

### Test Categories
- **Unit tests**: Individual service methods
- **Integration tests**: API endpoints with database
- **AI tests**: Prompt templates and responses
- **UI tests**: Frontend components and flows

### Running Tests
```bash
# All tests
pytest

# Specific test categories
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest --cov=app tests/
```

## 📁 File Structure Details

Each module file includes headers with:
- **Creation time** 
- **File name**
- **Specific purpose/function** 
- **Module boundaries**

Example:
```python
"""
LLM Router Configuration
File: app/agentic_core/llm_router/__init__.py
Created: 2025-07-17
Purpose: Dynamic LLM model selection for cost optimization
"""
```

## ⚠️ Production Considerations

### Scaling Path
1. **Monitor specific modules** for high load (Interview scoring, Resume generation)
2. **Extract modules** to microservices using Strangler Fig pattern
3. **Deploy independently** with load balancing

### Security Checklist
- [ ] Change default `.env` values in production
- [ ] Use secrets management for API keys
- [ ] Implement rate limiting
- [ ] Set up monitoring and alerts
- [ ] Configure proper CORS settings

## 🚀 Next Steps

1. **Sprint 0**: Complete project scaffolding ✓
2. **Sprint 1-3**: Implement Basic Interview Prep MVP
3. **Sprint 4-6**: Add RAG capabilities and document processing
4. **Sprint 7-9**: Advanced features and productization

## 📞 Support & Contributions

- **Issues**: Create issues in GitHub for bugs and feature requests
- **Contributions**: Follow CONTRIBUTING.md for contribution guidelines
- **Documentation**: Enhanced documentation at `/docs` (coming soon)

---

**Built with ❤️ using the Modular Monolith architecture - designed for sustainable growth**