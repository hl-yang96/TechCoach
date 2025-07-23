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
from llama_index.core import VectorStoreIndex, StorageContext, Settings, SimpleDirectoryReader, Document
from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser
from llama_index.core.node_parser.text.utils import split_by_sep
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.readers.file.unstructured import UnstructuredReader


from .chroma_client import ChromaDBClient
from .config import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_BATCH_SIZE,
    COLLECTION_CONFIGS,
    COLLECTION_PROJECTS_EXPERIENCE,
    get_collection_config,
    get_chunk_config,
    get_retrieval_config
)
from .document_processor import get_document_processor

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
        self.document_processor = get_document_processor()
        Settings.embed_model = GoogleGenAIEmbedding(
            model_name=EMBEDDING_MODEL_NAME,
            api_key=os.getenv("GEMINI_API_KEY"),
            embed_batch_size=EMBEDDING_BATCH_SIZE
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

            # Rebuild retrievers for existing collections with data
            await self._rebuild_all_retrievers()

            logger.info("Document Store initialized successfully with all collections")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Document Store: {e}")
            return False

    async def _initialize_collections(self):
        """Initialize all document collections based on user stories."""
        for collection_type, config in COLLECTION_CONFIGS.items():
            try:
                self.chroma_client.get_or_create_collection(
                    name=config["name"],
                    metadata=config["metadata"]
                )
                logger.info(f"Initialized collection: {config['name']} ({collection_type})")

            except Exception as e:
                logger.warning(f"Failed to initialize collection for {collection_type}: {e}")

    async def _rebuild_all_retrievers(self):
        """Rebuild retrievers for all collections that have data."""
        for collection_type in COLLECTION_CONFIGS.keys():
            try:
                await self._rebuild_retriever_for_collection(collection_type)
            except Exception as e:
                logger.warning(f"Failed to rebuild retriever for {collection_type}: {e}")
                continue

    async def _rebuild_retriever_for_collection(self, collection_type: str):
        """Rebuild retriever for a specific collection if it has data."""
        try:
            if collection_type in self.retrievers:
                logger.debug(f"Retriever for {collection_type} already exists")
                return

            config = COLLECTION_CONFIGS.get(collection_type)
            if not config:
                logger.warning(f"No config found for collection type: {collection_type}")
                return

            collection_name = config["name"]

            # Try to get existing collection
            try:
                collection = self.chroma_client.client.get_collection(name=collection_name)
                count = collection.count()

                if count > 0:
                    logger.info(f"Found {count} documents in collection {collection_type}, rebuilding retriever...")

                    # Create ChromaVectorStore and index
                    from llama_index.vector_stores.chroma import ChromaVectorStore
                    from llama_index.core import VectorStoreIndex

                    vector_store = ChromaVectorStore(chroma_collection=collection)
                    index = VectorStoreIndex.from_vector_store(vector_store)

                    self.indexes[collection_type] = index

                    # Create retriever with collection-specific configuration
                    retrieval_config = get_retrieval_config(collection_type)
                    self.retrievers[collection_type] = index.as_retriever(
                        similarity_top_k=retrieval_config["similarity_top_k"]
                    )

                    logger.info(f"Successfully rebuilt retriever for {collection_type} ({count} documents)")
                else:
                    logger.debug(f"Collection {collection_type} is empty, skipping retriever creation")

            except Exception as collection_error:
                logger.debug(f"Collection {collection_type} not found or inaccessible: {collection_error}")

        except Exception as e:
            logger.warning(f"Failed to rebuild retriever for {collection_type}: {e}")

    def ingest_documents(self, documents_path: str, collection_type: Optional[str] = None) -> bool:
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

    def ingest_single_document(self, document_path: str = None, document_content: str = None) -> Dict[str, Any]:
        """
        Comprehensive document ingestion including preprocessing and vector storage.

        This function combines preprocessing and ingestion into a single operation:
        1. Extract content from file or use provided content
        2. LLM-based preprocessing (rename, description, abstract, cleaning, classification)
        3. Ingest into ChromaDB vector store
        4. Return complete ingestion results

        Args:
            document_path: Path to the document file (optional)
            document_content: Raw text content (optional)

        Returns:
            Dictionary containing ingestion results:
            - success: Boolean indicating success/failure
            - document_id: Generated document ID
            - collection_type: Determined collection type
            - renamed_filename: Generated meaningful filename
            - description: Brief description
            - abstract: Detailed summary
            - cleaned_content: Normalized text content
            - chroma_document_ids: List of ChromaDB document IDs
            - file_path: Path to saved processed file
            - file_size: Size of processed content
            - error: Error message if failed
        """
        from datetime import datetime
        import uuid

        document_id = str(uuid.uuid4())
        temp_file_path = None

        try:
            # ========== PREPROCESSING PHASE ==========
            # 0. Create temp directories if they don't exist
            temp_dir = Path("app_data/temp/documents")
            temp_dir.mkdir(parents=True, exist_ok=True)

            # Save raw content to temporary file if no document_path provided
            if document_path is None and document_content is not None:
                # Create temporary file with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                temp_file_path = temp_dir / f"temp_doc_{timestamp}.txt"
                with open(temp_file_path, 'w', encoding='utf-8') as f:
                    f.write(document_content)
                document_path = str(temp_file_path)
                logger.info(f"Saved raw content to temporary file: {temp_file_path}")
            elif document_path is None:
                return {"success": False, "error": "Either document_path or document_content must be provided"}

            # 1. Use UnstructuredReader to extract structured data
            reader = UnstructuredReader()
            documents = reader.load_data(file=Path(document_path))
            logger.info(f"Finish extracting structured data from {document_path}")

            if not documents:
                return {"success": False, "error": f"No content could be extracted from {document_path}"}

            # Get the main document content
            main_document = documents[0]
            content = main_document.text
            original_filename = Path(document_path).name if document_path else "未知文档"

            logger.info(f"Extracted {len(content)} characters from document")

            limit=7000
            if len(content) >= 7000:
                logger.warning(f"Document content is very large ({len(content)} characters>{limit}), consider chunking")

            # 2. Send data content to LLM for comprehensive preprocessing
            preprocessing_result = self.document_processor.process_document(content[0:limit], original_filename)

            # Extract all preprocessing results
            collection_type = preprocessing_result.get("collection_type", COLLECTION_PROJECTS_EXPERIENCE)
            renamed_filename = preprocessing_result.get("renamed_filename", original_filename)
            description = preprocessing_result.get("description", "")
            abstract = preprocessing_result.get("abstract", "")
            cleaned_content = preprocessing_result.get("cleaned_content", content)
            base_metadata = preprocessing_result.get("metadata", {})

            # Determine final filename
            final_filename = renamed_filename
            if not final_filename.endswith('.txt'):
                final_filename += ".txt"

            # 3. Save the processed document to permanent location
            documents_dir = Path("app_data/documents")
            documents_dir.mkdir(parents=True, exist_ok=True)
            permanent_file_path = documents_dir / final_filename

            # Save cleaned content to permanent file
            with open(permanent_file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            logger.info(f"Saved processed document to: {permanent_file_path}")

            # ========== INGESTION PHASE ==========
            # Create processed document with enhanced metadata using cleaned content
            document = Document(
                text=cleaned_content,
                metadata={
                    "document_id": document_id,
                    "file_name": final_filename,
                    "description": description,
                    "collection_type": collection_type,
                    **base_metadata
                }
            )

            # Get collection configuration
            config = get_collection_config(collection_type)
            if not config:
                return {
                    "success": False,
                    "error": f"Unknown collection type: {collection_type}"
                }

            # Configure chunking based on collection type
            chunk_config = get_chunk_config(collection_type)

            node_parser = SentenceSplitter(
                chunk_size=chunk_config["chunk_size"],
                chunk_overlap=chunk_config["chunk_overlap"],
                separator="，,。？！；\n",
                paragraph_separator="---"
            )

            node_parser_2 = SemanticSplitterNodeParser(
                buffer_size=1,
                breakpoint_percentile_threshold=70,
                embed_model= Settings.embed_model,
                sentence_splitter=split_by_sep("\n", keep_sep=False),
            )
            
            selected_parser = node_parser_2

            # Get or create ChromaDB collection
            chroma_collection = self.chroma_client.get_or_create_collection(
                name=config["name"],
                metadata=config["metadata"]
            )
            logger.info(f"Get collection {collection_type}, start to ingest")

            # Create vector store and storage context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # Create or update index for this collection
            if collection_type in self.indexes:
                # Add document to existing index
                inserted_nodes = self.indexes[collection_type].insert(document)
                # Collect node IDs from inserted nodes
                chroma_document_ids = [node.node_id for node in inserted_nodes] if inserted_nodes else []
            else:
                # Create new index with custom node parser
                index = VectorStoreIndex.from_documents(
                    [document],
                    storage_context=storage_context,
                    transformations=[selected_parser]
                )
                self.indexes[collection_type] = index

                # Create retriever with collection-specific configuration
                retrieval_config = get_retrieval_config(collection_type)
                self.retrievers[collection_type] = index.as_retriever(
                    similarity_top_k=retrieval_config["similarity_top_k"]
                )

                # Get node IDs from the created index
                chroma_document_ids = []
                try:
                    # Try to get the document nodes from the index
                    docstore = index.docstore
                    if docstore and hasattr(docstore, 'docs'):
                        chroma_document_ids = list(docstore.docs.keys())
                except Exception as e:
                    logger.warning(f"Could not retrieve document IDs: {e}")

            # Store the ChromaDB document IDs in the document metadata for later use
            document.metadata["chroma_document_ids"] = chroma_document_ids

            logger.info(f"Successfully ingested document into {collection_type}: {final_filename}, ChromaDB IDs: {chroma_document_ids}")

            # ========== RETURN RESULTS ==========
            return {
                "success": True,
                "document_id": document_id,
                "collection_type": collection_type,
                "description": description,
                "abstract": abstract,
                "cleaned_content": cleaned_content,
                "chroma_document_ids": chroma_document_ids,
                "file_path": str(permanent_file_path),
                "file_size": len(cleaned_content.encode('utf-8')),
                "final_filename": final_filename
            }

        except Exception as e:
            logger.error(f"Failed to ingest single document: {e}")
            return {
                "success": False,
                "error": str(e),
                "document_id": document_id
            }
        finally:
            # Clean up temporary file if it was created from raw content
            if temp_file_path and temp_file_path.exists():
                try:
                    temp_file_path.unlink()
                    logger.info(f"Cleaned up temporary file: {temp_file_path}")
                except Exception as cleanup_error:
                    logger.warning(f"Failed to cleanup temporary file {temp_file_path}: {cleanup_error}")
    
    def search_documents(self,
                        query_text: str,
                        collection_types: Optional[List[str]] = None,
                        top_k: int = 5) -> List[Dict[str, Any]]:
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
