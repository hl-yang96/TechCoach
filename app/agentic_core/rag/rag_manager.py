"""
RAG Manager for TechCoach
File: app/agentic_core/rag/rag_manager.py
Purpose: Document vectorization, storage and retrieval infrastructure for CrewAI agents
"""

import os
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

# LlamaIndex imports for document processing and vector storage
from llama_index.core import VectorStoreIndex, StorageContext, Settings, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import NodeWithScore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

from .chroma_client import ChromaDBClient
from .config import EMBEDDING_MODEL_NAME, EMBEDDING_BATCH_SIZE

logger = logging.getLogger(__name__)


class RAGManager:
    """
    Document Storage and Retrieval Manager for TechCoach.

    This class provides infrastructure for CrewAI agents:
    - Document vectorization and storage
    - Semantic similarity search
    - Document metadata management
    - Vector database operations

    Note: This class does NOT handle LLM generation - that's handled by CrewAI agents.
    """
    
    # Default collection for general documents
    DEFAULT_COLLECTION = {
        "name": "techcoach_test",
        "description": "General document storage",
        "metadata": {"type": "general", "purpose": "storage"}
    }
    
    def __init__(self, chroma_host: Optional[str] = None, chroma_port: Optional[int] = None):
        """
        Initialize RAG Manager.
        
        Args:
            chroma_host: ChromaDB host
            chroma_port: ChromaDB port
        """
        self.chroma_client = ChromaDBClient(host=chroma_host, port=chroma_port)
        self.index: Optional[VectorStoreIndex] = None
        self.query_engine: Optional[Any] = None
        self._setup_llama_index()
        
    def _setup_llama_index(self):
        """Configure LlamaIndex global settings."""
        # Configure LLM
        Settings.llm = OpenAI(
            model="gpt-4o-mini",  # Using cost-effective model for most operations
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Configure embedding model
        Settings.embed_model = GoogleGenAIEmbedding(
            model_name=EMBEDDING_MODEL_NAME,  # Google Gemini embedding model
            api_key=os.getenv("GEMINI_API_KEY"),
            embed_batch_size=EMBEDDING_BATCH_SIZE
        )
        
        # Configure text splitter
        Settings.node_parser = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separator=" "
        )
        
        logger.info("LlamaIndex settings configured")
    
    async def initialize(self) -> bool:
        """
        Initialize RAG system.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Connect to ChromaDB
            if not self.chroma_client.connect():
                logger.error("Failed to connect to ChromaDB")
                return False
            
            # Initialize predefined collections
            await self._initialize_collections()
            
            logger.info("RAG Manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Manager: {e}")
            return False
    
    async def _initialize_collections(self):
        """Initialize default collection."""
        try:
            self.chroma_client.get_or_create_collection(
                name=self.DEFAULT_COLLECTION["name"],
                metadata=self.DEFAULT_COLLECTION["metadata"]
            )
            logger.info(f"Initialized collection: {self.DEFAULT_COLLECTION['name']}")
        except Exception as e:
            logger.error(f"Failed to initialize collection {self.DEFAULT_COLLECTION['name']}: {e}")
    
    def ingest_documents(self, documents_path: str) -> bool:
        """
        Ingest documents from a directory into default collection.

        Args:
            documents_path: Path to directory containing documents

        Returns:
            True if ingestion successful, False otherwise
        """
        try:
            # Load documents
            documents = SimpleDirectoryReader(documents_path).load_data()
            if not documents:
                logger.warning(f"No documents found in {documents_path}")
                return False

            # Get or create ChromaDB collection
            chroma_collection = self.chroma_client.get_or_create_collection(
                name=self.DEFAULT_COLLECTION["name"],
                metadata=self.DEFAULT_COLLECTION["metadata"]
            )

            # Create vector store
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # Create index
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context
            )

            # Store index and create query engine
            self.index = index
            self.query_engine = index.as_query_engine()

            logger.info(f"Successfully ingested {len(documents)} documents into {self.DEFAULT_COLLECTION['name']}")
            return True

        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            return False
    
    def query(self, query_text: str) -> Optional[str]:
        """
        Query the RAG system.

        Args:
            query_text: Query string

        Returns:
            Query response or None if failed
        """
        if not self.query_engine:
            logger.error("No query engine available. Please ingest documents first.")
            return None

        try:
            response = self.query_engine.query(query_text)
            return str(response)
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics for the default collection."""
        try:
            info = self.chroma_client.get_collection_info(self.DEFAULT_COLLECTION["name"])
            return {
                "name": self.DEFAULT_COLLECTION["name"],
                "description": self.DEFAULT_COLLECTION["description"],
                "document_count": info.get("count", 0),
                "has_index": self.index is not None
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}

    def reset_collection(self) -> bool:
        """
        Reset the default collection (delete all data).

        Returns:
            True if reset successful, False otherwise
        """
        try:
            # Delete collection from ChromaDB
            success = self.chroma_client.delete_collection(self.DEFAULT_COLLECTION["name"])

            # Remove from local cache
            self.index = None
            self.query_engine = None

            # Recreate empty collection
            if success:
                self.chroma_client.get_or_create_collection(
                    name=self.DEFAULT_COLLECTION["name"],
                    metadata=self.DEFAULT_COLLECTION["metadata"]
                )

            logger.info(f"Reset collection: {self.DEFAULT_COLLECTION['name']}")
            return success

        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")
            return False
