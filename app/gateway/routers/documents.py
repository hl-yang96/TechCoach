"""
Document Store API Router
File: app/gateway/routers/documents.py
Purpose: API endpoints for document storage and retrieval (for CrewAI agents)
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agentic_core.rag.document_store import DocumentStore
from app.agentic_core.rag.chroma_client import ChromaDBClient

logger = logging.getLogger(__name__)
router = APIRouter()

# Global document store instance
document_store: Optional[DocumentStore] = None


class SearchRequest(BaseModel):
    query: str
    collection_types: Optional[List[str]] = None
    top_k: int = 5


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_results: int
    collections_searched: List[str]
    success: bool


class ContextRequest(BaseModel):
    query: str
    collection_types: Optional[List[str]] = None
    max_tokens: int = 2000

class IngestDocumentsRequest(BaseModel):
    documents_path: str
    collection_type: Optional[str] = None


class ContextResponse(BaseModel):
    context: str
    token_count: int
    collections_searched: List[str]
    success: bool


class CollectionStatsResponse(BaseModel):
    collection: Dict[str, Any]


class CollectionInfoRequest(BaseModel):
    collection_type: str


class CollectionInfoResponse(BaseModel):
    collection_info: Dict[str, Any]
    success: bool


class ResetCollectionRequest(BaseModel):
    collection_type: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    chroma_connected: bool
    store_initialized: bool
    ready_for_agents: bool
    message: str


async def get_document_store() -> DocumentStore:
    """Get or create document store instance."""
    global document_store
    if document_store is None:
        document_store = DocumentStore()
        if not await document_store.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize document store")
    return document_store


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check document store health."""
    try:
        # Test ChromaDB connection
        chroma_client = ChromaDBClient()
        chroma_connected = chroma_client.connect()
        
        # Test document store
        store_initialized = False
        ready_for_agents = False
        try:
            store = await get_document_store()
            store_initialized = True
            ready_for_agents = store.is_ready()
        except Exception:
            pass
        
        status = "healthy" if chroma_connected and store_initialized else "unhealthy"
        message = "Document store is ready for CrewAI agents" if ready_for_agents else "Document store needs documents"
        
        return HealthResponse(
            status=status,
            chroma_connected=chroma_connected,
            store_initialized=store_initialized,
            ready_for_agents=ready_for_agents,
            message=message
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="error",
            chroma_connected=False,
            store_initialized=False,
            ready_for_agents=False,
            message=f"Health check error: {str(e)}"
        )


@router.get("/stats", response_model=CollectionStatsResponse)
async def get_collection_stats():
    """Get statistics for the document collection."""
    try:
        store = await get_document_store()
        stats = store.get_collection_stats()
        
        return CollectionStatsResponse(collection=stats)
    except Exception as e:
        logger.error(f"Failed to get collection stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get collection stats: {str(e)}")


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Search for similar documents across specified collections (for CrewAI agents)."""
    try:
        store = await get_document_store()

        # Perform search
        results = store.search_documents(
            query_text=request.query,
            collection_types=request.collection_types,
            top_k=request.top_k
        )

        # Get collections that were searched
        collections_searched = request.collection_types or store.get_available_collections()

        return SearchResponse(
            results=results,
            total_results=len(results),
            collections_searched=collections_searched,
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/context", response_model=ContextResponse)
async def get_context_for_agents(request: ContextRequest):
    """Get concatenated document context for CrewAI agents from specified collections."""
    try:
        store = await get_document_store()

        # Get context
        context = store.get_document_context(
            query_text=request.query,
            collection_types=request.collection_types,
            max_tokens=request.max_tokens
        )

        # Estimate token count
        token_count = len(context) // 4  # Rough approximation

        # Get collections that were searched
        collections_searched = request.collection_types or store.get_available_collections()

        return ContextResponse(
            context=context,
            token_count=token_count,
            collections_searched=collections_searched,
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Context generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Context generation failed: {str(e)}")


@router.post("/ingest")
async def ingest_documents(request: IngestDocumentsRequest):
    """Ingest documents with automatic classification or into specified collection."""
    try:
        store = await get_document_store()

        # Ingest documents
        success = store.ingest_documents(
            documents_path=request.documents_path,
            collection_type=request.collection_type
        )

        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to ingest documents from {request.documents_path}"
            )

        classification_mode = "automatic LLM classification" if request.collection_type is None else f"specified collection: {request.collection_type}"

        return {
            "message": f"Successfully ingested documents using {classification_mode}",
            "documents_path": request.documents_path,
            "collection_type": request.collection_type,
            "classification_mode": classification_mode,
            "success": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Document ingestion failed: {str(e)}")


@router.delete("/reset")
async def reset_collection(request: ResetCollectionRequest = None):
    """Reset (clear all data from) document collection(s)."""
    try:
        store = await get_document_store()

        collection_type = request.collection_type if request else None

        # Reset collection(s)
        success = store.reset_collection(collection_type)

        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to reset collection(s)"
            )

        reset_message = f"all collections" if collection_type is None else f"collection: {collection_type}"

        return {
            "message": f"Successfully reset {reset_message}",
            "collection_type": collection_type,
            "success": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Collection reset failed: {e}")
        raise HTTPException(status_code=500, detail=f"Collection reset failed: {str(e)}")


@router.get("/ready")
async def check_agent_readiness():
    """Check if document store is ready for CrewAI agents."""
    try:
        store = await get_document_store()
        ready = store.is_ready()
        available_collections = store.get_available_collections()

        return {
            "ready_for_agents": ready,
            "available_collections": available_collections,
            "total_collections": len(available_collections),
            "message": "Document store is ready for CrewAI agents" if ready else "Please ingest documents first",
            "success": True
        }

    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Readiness check failed: {str(e)}")


@router.get("/collections")
async def list_collections():
    """List all available collection types and their configurations."""
    try:
        from app.agentic_core.rag.config import COLLECTION_CONFIGS

        return {
            "collections": COLLECTION_CONFIGS,
            "total_collections": len(COLLECTION_CONFIGS),
            "success": True
        }

    except Exception as e:
        logger.error(f"Failed to list collections: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")


@router.get("/collections/{collection_type}", response_model=CollectionInfoResponse)
async def get_collection_info(collection_type: str):
    """Get detailed information about a specific collection."""
    try:
        store = await get_document_store()
        collection_info = store.get_collection_info(collection_type)

        return CollectionInfoResponse(
            collection_info=collection_info,
            success=True
        )

    except Exception as e:
        logger.error(f"Failed to get collection info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get collection info: {str(e)}")
