"""
Main RAG pipeline coordinator
"""
from typing import List, Dict, Any, Optional
from .loader import DocumentLoader, Document
from .chunker import create_chunks, Chunk
from .embeddings import embed_chunks
from .vector_store import FAISSVectorStore
from .retriever import RAGRetriever
from .llm import RAGPipeline


class RAGSystem:
    """Complete RAG system"""
    
    def __init__(self, llm_model: str = "llama2", 
                embedding_model: str = "nomic-embed-text",
                chunk_size: int = 512,
                chunk_overlap: int = 64,
                vector_store_path: Optional[str] = None):
        """
        Initialize RAG system
        
        Args:
            llm_model: LLM model name
            embedding_model: Embedding model name
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            vector_store_path: Path to save/load vector store
        """
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_store_path = vector_store_path
        
        self.vector_store = None
        self.retriever = None
        self.rag_pipeline = RAGPipeline(llm_model, embedding_model)
        self.documents = []
        self.chunks = []
    
    def load_pdf(self, file_path: str) -> None:
        """Load PDF document"""
        docs = DocumentLoader.load_pdf(file_path)
        self.documents.extend(docs)
        self._process_documents()
    
    def load_web(self, url: str) -> None:
        """Load web document"""
        docs = DocumentLoader.load_web(url)
        self.documents.extend(docs)
        self._process_documents()
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to system"""
        self.documents.extend(documents)
        self._process_documents()
    
    def _process_documents(self) -> None:
        """Process documents: chunk, embed, and index"""
        if not self.documents:
            return
        
        # Create chunks
        chunks = create_chunks(
            self.documents,
            chunk_size=self.chunk_size,
            overlap=self.chunk_overlap
        )
        self.chunks.extend(chunks)
        
        # Embed chunks
        embeddings, embedding_dim = embed_chunks(
            self.chunks,
            model=self.embedding_model
        )
        
        # Create/update vector store
        if self.vector_store is None:
            self.vector_store = FAISSVectorStore(embedding_dim=embedding_dim)
        
        # Add to vector store
        metadata = [chunk.metadata for chunk in self.chunks]
        texts = [chunk.content for chunk in self.chunks]
        self.vector_store.add_vectors(embeddings, metadata, texts)
        
        # Create retriever
        self.retriever = RAGRetriever(self.vector_store, self.embedding_model)
    
    def query(self, question: str, k: int = 5) -> Dict[str, Any]:
        """
        Query the system
        
        Args:
            question: User question
            k: Number of documents to retrieve
        
        Returns:
            Dictionary with answer, sources, and metadata
        """
        if self.retriever is None:
            raise ValueError("No documents loaded. Please load documents first.")
        
        # Retrieve relevant documents
        retrieved = self.retriever.retrieve(question, k=k)
        
        # Generate answer with sources
        result = self.rag_pipeline.answer(question, retrieved)
        
        return result
    
    def save_vector_store(self, path: str) -> None:
        """Save vector store to disk"""
        if self.vector_store is None:
            raise ValueError("No vector store to save")
        self.vector_store.save(path)
    
    def load_vector_store(self, path: str) -> None:
        """Load vector store from disk"""
        self.vector_store = FAISSVectorStore.load(path)
        self.retriever = RAGRetriever(self.vector_store, self.embedding_model)
    
    def clear(self) -> None:
        """Clear all data"""
        self.documents = []
        self.chunks = []
        self.vector_store = None
        self.retriever = None
