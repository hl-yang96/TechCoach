# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TechCoach** is an AI-powered personalized career coaching platform designed for tech professionals. The system combines RAG (Retrieval Augmented Generation) with Agentic AI to provide customized interview preparation, resume optimization, and career guidance based on individual's code, projects, and career history.

### Core Architecture

**Architecture Pattern**: Modular Monolith with "Distribu-Ready" design
- Single Docker container deployment
- Process-level module boundaries
- Future-ready for microservice extraction via Strangler Fig Pattern

**Key Modules**:
- WebApp Gateway (FastAPI) - API routing and orchestration
- Ingestion Module - Data ingestion (Git repos, PDFs, docs)
- Agentic Core - AI orchestration with LLM routing
- Interview Prep - Interview question generation and practice
- Career Docs - Resume optimization and analysis
- Shared Kernel - Common data structures and interfaces

### Technology Stack

**Backend**:
- **Framework**: FastAPI (Python)
- **RAG Framework**: LlamaIndex (core) + CrewAI (workflows) + LangChain (tools)
- **Vector Database**: ChromaDB (local Docker deployment)
- **State**: SQLite for relationships, ChromaDB for embeddings
- **AI Integration**: LLM Router for multi-provider support (OpenAI, Anthropic, etc.)

**Frontend**:
- **Framework**: Vue.js 3
- **Management**: Pinia (state) + Vue Router

### Development Commands

#### Setup & Environment
```bash
# Initial project setup (follow modular monolith structure)
# Directory structure: /app/gateway, /app/agentic_core, /app/interview_prep, etc.

# Build and start all services
docker-compose up --build

# Local development without Docker (when needed)
uvicorn app.main:app --reload --port 8001
```

#### Core Development Commands
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Linting
ruff check .
black .

# Type checking
mypy app/

# Generate new RAG service components
python scripts/generate_module.py interview_prep

# Vector database operations
python scripts/reset_chroma.py
```

### Project Structure

```
TechCoach/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry
│   ├── gateway/                 # API endpoints and routing
│   ├── agentic_core/            # AI orchestration and RAG
│   ├── interview_prep/          # Interview related business logic
│   ├── career_docs/             # Resume optimization
│   ├── ingestion/               # Data ingestion handlers
│   └── shared_kernel/           # Common models and utilities
├── frontend/
│   ├── src/
│   ├── vite.config.js
│   └── package.json
├── docker-compose.yml           # Multi-service orchestration
├── Dockerfile                   # Backend container
├── requirements.txt             # Python dependencies
└── tests/
    ├── integration/
    └── unit/
```

### LLM Router Configuration

The system includes a sophisticated LLM Router that determines optimal model selection based on:
- **Rule-based routing** for deterministic tasks
- **Semantic similarity** for context-aware routing
- **LLM-as-classifier** for complex requests

Configuration location: `config/llm_router.yaml`

### Key Implementation Patterns

1. **RAG Pipeline Flow**: 
   ```
   Document upload → Chunking → Embedding → ChromaDB storage → Retrieval → Context injection → LLM response
   ```

2. **Agent Patterns**:
   - **Librarian**: High-fidelity retrieval for project analysis
   - **Coach**: Generative and evaluative patterns for interview prep

3. **Data Persistence**:
   - ChromaDB: Vector embeddings and semantic search
   - SQLite: User sessions, generated content, relationships

### Development Environment

**Required Environment Variables**:
```bash
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here  # optional for alternative providers
CHROMA_HOST=chroma  # in Docker
CHROMA_PORT=8000
DB_PATH=./app_data/sqlite.db
```

**Local Development Setup**:
1. Clone repository
2. Set up Python virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables in `.env`
5. Start services: `docker-compose up`

### Common Development Tasks

**Adding New RAG Pipeline**:
1. Create new module in `app/agentic_core/rag/[module_name]`
2. Configure LlamaIndex index and storage contexts
3. Add endpoints in `app/gateway/routers/[module_name].py`

**Schema Changes**:
1. Update models in `app/shared_kernel/models.py`
2. Run migrations: `alembic revision --autogenerate`
3. Update frontend types: `npm run generate-types` (frontend)

**Testing AI Components**:
1. Use MockLLM for unit testing
2. Integration tests against real LLM APIs with cost limits
3. Test prompts in `tests/prompts/`

### Production Considerations

**Scaling Path**:
- Modular monolith allows service extraction
- Key candidates for microservice extraction: Interview scoring (high compute), Resume generation (high memory)
- Use Strangler Fig pattern for gradual migration

**Monitoring**:
- FastAPI middleware for request/response timing
- LLM cost tracking via router logs
- Vector db query performance monitoring

This foundation provides a scalable architecture for an AI career coaching platform while maintaining development simplicity for independent deployment.