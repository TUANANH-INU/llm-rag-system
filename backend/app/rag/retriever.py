"""
Retriever for RAG pipeline
"""
from typing import List, Dict, Tuple, Any, Optional
import numpy as np
from .vector_store import FAISSVectorStore
from .embeddings import OllamaEmbeddings


class RAGRetriever:
    """Retrieve relevant documents for a query"""
    
    def __init__(self, vector_store: FAISSVectorStore, 
                 embedding_model: str = "nomic-embed-text"):
        """
        Initialize retriever
        
        Args:
            vector_store: Vector store instance
            embedding_model: Embedding model name
        """
        self.vector_store = vector_store
        self.embeddings = OllamaEmbeddings(model=embedding_model)
    
    def retrieve(self, query: str, k: int = 5, 
                score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Query string
            k: Number of results to return
            score_threshold: Minimum similarity score
        
        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed(query)
        
        # Search in vector store
        results, distances = self.vector_store.search(query_embedding, k=k)
        
        # Filter by score threshold
        filtered_results = [
            r for r in results 
            if r["score"] >= score_threshold
        ]
        
        return filtered_results
    
    def retrieve_with_context(self, query: str, k: int = 5, 
                             context_window: int = 1) -> List[Dict[str, Any]]:
        """
        Retrieve documents with additional context
        
        Args:
            query: Query string
            k: Number of results to return
            context_window: Number of adjacent chunks to include
        
        Returns:
            List of documents with context
        """
        results = self.retrieve(query, k=k)
        
        # Add context from adjacent chunks
        for result in results:
            chunk_id = result["metadata"].get("chunk_id", 0)
            source = result["metadata"].get("source", "")
            
            # Find context chunks (simplified - could be enhanced)
            result["context"] = {
                "chunk_id": chunk_id,
                "source": source
            }
        
        return results


def format_retrieval_results(results: List[Dict[str, Any]]) -> str:
    """
    Format retrieval results for display
    
    Args:
        results: List of retrieval results
    
    Returns:
        Formatted string
    """
    formatted = ""
    
    for i, result in enumerate(results, 1):
        formatted += f"\n{'='*60}\n"
        formatted += f"[{i}] {result['text']}\n"
        formatted += f"Source: {result['metadata'].get('source', 'Unknown')}\n"
        formatted += f"Confidence: {result['score']:.2%}\n"
    
    return formatted
