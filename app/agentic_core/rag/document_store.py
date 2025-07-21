"""
Document Store for TechCoach
File: app/agentic_core/rag/document_store.py
Purpose: Document vectorization, storage and retrieval infrastructure for CrewAI agents
"""

import os,sys
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

# LlamaIndex imports for document processing and vector storage
from llama_index.core import VectorStoreIndex, StorageContext, Settings, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

from .chroma_client import ChromaDBClient
from .config import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_BATCH_SIZE,
    COLLECTION_CONFIGS,
    CollectionType,
    get_collection_config,
    get_chunk_config,
    get_retrieval_config
)
from .document_classifier import get_document_classifier

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentStore:
    """
    Document Storage and Retrieval Infrastructure for CrewAI Agents.

    This class provides core document management capabilities:
    - Document ingestion and vectorization with LLM-based classification
    - Semantic similarity search across multiple collections
    - Document metadata management with automatic enhancement
    - Vector database operations for job-seeking profile management

    Design Philosophy:
    - NO LLM generation (handled by CrewAI agents)
    - Focus on storage and retrieval
    - Provide rich context for agents
    - Support multiple specialized collections based on user stories
    """
    
    def __init__(self, chroma_host: Optional[str] = None, chroma_port: Optional[int] = None):
        """
        Initialize Document Store.

        Args:
            chroma_host: ChromaDB host
            chroma_port: ChromaDB port
        """
        self.chroma_client = ChromaDBClient(host=chroma_host, port=chroma_port)
        self.indexes: Dict[str, VectorStoreIndex] = {}  # Multiple indexes for different collections
        self.retrievers: Dict[str, Any] = {}  # Multiple retrievers for different collections
        self.document_classifier = get_document_classifier()
        self._setup_embedding_config()
        
    def _setup_embedding_config(self):
        """Configure embedding model for document vectorization."""
        # Only configure embedding model - no LLM needed
        Settings.embed_model = GoogleGenAIEmbedding(
            model_name=EMBEDDING_MODEL_NAME,
            api_key=os.getenv("GEMINI_API_KEY"),
            embed_batch_size=EMBEDDING_BATCH_SIZE
        )
        
        # Configure text splitter for optimal chunking
        Settings.node_parser = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separator=" "
        )
        
        logger.info("Document Store configured for embedding and chunking")
    
    async def initialize(self) -> bool:
        """
        Initialize document storage system with all collections.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Connect to ChromaDB
            if not self.chroma_client.connect():
                logger.error("Failed to connect to ChromaDB")
                return False

            # Initialize all collections based on user stories
            await self._initialize_collections()

            logger.info("Document Store initialized successfully with all collections")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Document Store: {e}")
            return False

    async def _initialize_collections(self):
        """Initialize all document collections based on user stories."""
        try:
            for collection_type, config in COLLECTION_CONFIGS.items():
                self.chroma_client.get_or_create_collection(
                    name=config["name"],
                    metadata=config["metadata"]
                )
                logger.info(f"Initialized collection: {config['name']} ({collection_type})")
        except Exception as e:
            logger.error(f"Failed to initialize collections: {e}")
    
    def ingest_documents(self, documents_path: str, collection_type: Optional[str] = None) -> bool:
        """
        Ingest documents with automatic classification and metadata generation.

        Args:
            documents_path: Path to directory containing documents
            collection_type: Optional specific collection type, if None will auto-classify

        Returns:
            True if ingestion successful, False otherwise
        """
        try:
            # Load documents
            if os.path.isdir(documents_path):
                documents = SimpleDirectoryReader(input_dir=documents_path).load_data()
            else:
                documents = SimpleDirectoryReader(input_files=[documents_path,]).load_data()
            if not documents:
                logger.warning(f"No documents found in {documents_path}")
                return False

            success_count = 0
            for document in documents:
                if self._ingest_single_document(document, collection_type):
                    success_count += 1

            logger.info(f"Successfully ingested {success_count}/{len(documents)} documents")
            return success_count > 0

        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            return False

    def _ingest_single_document(self, document: Any, collection_type: Optional[str] = None) -> bool:
        """
        Ingest a single document with classification and metadata enhancement.

        Args:
            document: LlamaIndex document object
            collection_type: Optional specific collection type

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get document content and filename
            content = document.text
            filename = getattr(document, 'metadata', {}).get('file_name', '')

            # Classify document if collection_type not specified
            if collection_type is None:
                collection_type, enhanced_metadata, final_filename = self.document_classifier.get_collection_and_metadata(
                    content, filename
                )
                # Update filename if it was generated
                if not filename or filename == "未知":
                    document.metadata["file_name"] = final_filename
            else:
                # Use provided collection type and enhance metadata
                base_metadata = getattr(document, 'metadata', {})
                enhanced_metadata = self.document_classifier.enhance_metadata(
                    collection_type, content, base_metadata
                )

            # Update document metadata
            document.metadata.update(enhanced_metadata)

            # Get collection configuration
            config = get_collection_config(collection_type)
            if not config:
                logger.error(f"Unknown collection type: {collection_type}")
                return False

            # Configure chunking based on collection type
            chunk_config = get_chunk_config(collection_type)
            node_parser = SentenceSplitter(
                chunk_size=chunk_config["chunk_size"],
                chunk_overlap=chunk_config["chunk_overlap"],
                separator=" "
            )

            # Get or create ChromaDB collection
            chroma_collection = self.chroma_client.get_or_create_collection(
                name=config["name"],
                metadata=config["metadata"]
            )

            # Create vector store and storage context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # Create or update index for this collection
            if collection_type in self.indexes:
                # Add document to existing index
                self.indexes[collection_type].insert(document)
            else:
                # Create new index with custom node parser
                index = VectorStoreIndex.from_documents(
                    [document],
                    storage_context=storage_context,
                    node_parser=node_parser
                )
                self.indexes[collection_type] = index

                # Create retriever with collection-specific configuration
                retrieval_config = get_retrieval_config(collection_type)
                self.retrievers[collection_type] = index.as_retriever(
                    similarity_top_k=retrieval_config["similarity_top_k"]
                )

            logger.info(f"Ingested document into {collection_type}: {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to ingest single document: {e}")
            return False
    
    def search_documents(self,
                        query_text: str,
                        collection_types: Optional[List[str]] = None,
                        top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents across specified collections.

        Args:
            query_text: Search query
            collection_types: List of collection types to search, if None searches all
            top_k: Number of top results to return per collection

        Returns:
            List of relevant document chunks with metadata
        """
        if not self.retrievers:
            logger.error("No retrievers available. Please ingest documents first.")
            return []

        # If no specific collections specified, search all available
        if collection_types is None:
            collection_types = list(self.retrievers.keys())

        try:
            all_results = []

            for collection_type in collection_types:
                if collection_type not in self.retrievers:
                    logger.warning(f"Collection {collection_type} not available")
                    continue

                # Get collection-specific top_k
                retrieval_config = get_retrieval_config(collection_type)
                collection_top_k = min(top_k, retrieval_config["similarity_top_k"])

                # Retrieve from this collection
                retriever = self.retrievers[collection_type]
                nodes = retriever.retrieve(query_text)

                # Process results
                for i, node in enumerate(nodes[:collection_top_k]):
                    result = {
                        "rank": i + 1,
                        "content": node.text,
                        "score": getattr(node, 'score', 0.0),
                        "metadata": node.metadata,
                        "source": node.metadata.get("source", "unknown"),
                        "node_id": node.node_id,
                        "collection_type": collection_type,
                        "collection_rank": i + 1
                    }
                    all_results.append(result)

            # Sort all results by score (descending)
            all_results.sort(key=lambda x: x["score"], reverse=True)

            # Re-rank and limit total results
            final_results = []
            for i, result in enumerate(all_results[:top_k * len(collection_types)]):
                result["overall_rank"] = i + 1
                final_results.append(result)

            logger.info(f"Retrieved {len(final_results)} documents from {len(collection_types)} collections")
            return final_results

        except Exception as e:
            logger.error(f"Document search failed: {e}")
            return []
    
    def get_document_context(self,
                            query_text: str,
                            collection_types: Optional[List[str]] = None,
                            max_tokens: int = 2000) -> str:
        """
        Get concatenated document context for CrewAI agents from specified collections.

        Args:
            query_text: Query to find relevant context
            collection_types: List of collection types to search
            max_tokens: Maximum tokens to return (approximate)

        Returns:
            Concatenated document context string with collection information
        """
        results = self.search_documents(query_text, collection_types, top_k=10)

        context_parts = []
        current_length = 0

        for result in results:
            content = result["content"]
            source = result["source"]
            collection_type = result["collection_type"]
            score = result["score"]

            # Estimate token count (rough approximation: 1 token ≈ 4 characters)
            estimated_tokens = len(content) // 4

            if current_length + estimated_tokens > max_tokens:
                break

            # Include collection type and relevance score in context
            context_header = f"[Collection: {collection_type} | Source: {source} | Score: {score:.3f}]"
            context_parts.append(f"{context_header}\n{content}\n")
            current_length += estimated_tokens

        context = "\n---\n".join(context_parts)
        collections_searched = collection_types or list(self.retrievers.keys())
        logger.info(f"Generated context with ~{current_length} tokens from collections: {collections_searched}")

        return context
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics for all document collections."""
        try:
            stats = {
                "total_collections": len(COLLECTION_CONFIGS),
                "active_collections": len(self.indexes),
                "collections": {}
            }

            for collection_type, config in COLLECTION_CONFIGS.items():
                try:
                    info = self.chroma_client.get_collection_info(config["name"])
                    collection_stats = {
                        "name": config["name"],
                        "description": config["description"],
                        "document_count": info.get("count", 0),
                        "has_index": collection_type in self.indexes,
                        "has_retriever": collection_type in self.retrievers,
                        "phase": config["metadata"].get("phase", 1),
                        "chunk_size": config["chunk_size"],
                        "similarity_top_k": config["similarity_top_k"]
                    }
                    stats["collections"][collection_type] = collection_stats
                except Exception as e:
                    stats["collections"][collection_type] = {"error": str(e)}

            return stats
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}
    
    def reset_collection(self, collection_type: Optional[str] = None) -> bool:
        """
        Reset document collection(s) (delete all data).

        Args:
            collection_type: Specific collection to reset, if None resets all

        Returns:
            True if reset successful, False otherwise
        """
        try:
            if collection_type:
                # Reset specific collection
                config = get_collection_config(collection_type)
                if not config:
                    logger.error(f"Unknown collection type: {collection_type}")
                    return False

                success = self.chroma_client.delete_collection(config["name"])

                # Clear local cache for this collection
                if collection_type in self.indexes:
                    del self.indexes[collection_type]
                if collection_type in self.retrievers:
                    del self.retrievers[collection_type]

                # Recreate empty collection
                if success:
                    self.chroma_client.get_or_create_collection(
                        name=config["name"],
                        metadata=config["metadata"]
                    )

                logger.info(f"Reset collection: {config['name']} ({collection_type})")
                return success
            else:
                # Reset all collections
                success_count = 0
                for collection_type, config in COLLECTION_CONFIGS.items():
                    try:
                        if self.chroma_client.delete_collection(config["name"]):
                            success_count += 1
                            # Recreate empty collection
                            self.chroma_client.get_or_create_collection(
                                name=config["name"],
                                metadata=config["metadata"]
                            )
                    except Exception as e:
                        logger.error(f"Failed to reset collection {collection_type}: {e}")

                # Clear all local caches
                self.indexes.clear()
                self.retrievers.clear()

                logger.info(f"Reset {success_count}/{len(COLLECTION_CONFIGS)} collections")
                return success_count > 0

        except Exception as e:
            logger.error(f"Failed to reset collection(s): {e}")
            return False

    def is_ready(self) -> bool:
        """Check if document store is ready for CrewAI agents."""
        return (
            self.chroma_client.is_connected() and
            len(self.indexes) > 0 and
            len(self.retrievers) > 0
        )

    def get_available_collections(self) -> List[str]:
        """Get list of available collection types."""
        return list(self.retrievers.keys())

    def get_collection_info(self, collection_type: str) -> Dict[str, Any]:
        """Get detailed information about a specific collection."""
        config = get_collection_config(collection_type)
        if not config:
            return {"error": f"Unknown collection type: {collection_type}"}

        try:
            info = self.chroma_client.get_collection_info(config["name"])
            return {
                "collection_type": collection_type,
                "name": config["name"],
                "description": config["description"],
                "document_count": info.get("count", 0),
                "has_index": collection_type in self.indexes,
                "has_retriever": collection_type in self.retrievers,
                "config": config
            }
        except Exception as e:
            return {"error": str(e)}
