"""
Embedding generation using Ollama
"""
import os
import json
from typing import List, Dict, Any
import requests
import numpy as np


class OllamaEmbeddings:
    """Generate embeddings using Ollama"""
    
    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://ollama:11434"):
        """
        Initialize Ollama embeddings
        
        Args:
            model: Ollama model name for embeddings
            base_url: Ollama server base URL
        """
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        self.embedding_dim = None
    
    def embed(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model, "input": text},
                timeout=300
            )
            response.raise_for_status()
            
            data = response.json()
            embedding = np.array(data["embeddings"][0], dtype=np.float32)
            
            if self.embedding_dim is None:
                self.embedding_dim = len(embedding)
            
            return embedding
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")
    
    def embed_batch(self, texts: List[str], batch_size: int = 10) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
        
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = []
            
            for text in batch:
                try:
                    embedding = self.embed(text)
                    batch_embeddings.append(embedding)
                except Exception as e:
                    print(f"Error embedding text: {e}")
                    # Use zero vector as fallback
                    batch_embeddings.append(np.zeros(self.embedding_dim or 384, dtype=np.float32))
            
            embeddings.extend(batch_embeddings)
        
        return embeddings


def embed_chunks(chunks: List, model: str = "nomic-embed-text", 
                batch_size: int = 10) -> tuple:
    """
    Embed a list of chunks
    
    Args:
        chunks: List of Chunk objects
        model: Embedding model
        batch_size: Batch size
    
    Returns:
        Tuple of (embeddings, embedding_dim)
    """
    embedder = OllamaEmbeddings(model=model)
    
    texts = [chunk.content for chunk in chunks]
    embeddings = embedder.embed_batch(texts, batch_size=batch_size)
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    # Get embedding dimension - ensure it's int and valid
    if len(embeddings_array) > 0:
        embedding_dim = int(embeddings_array.shape[1])
    else:
        embedding_dim = int(embedder.embedding_dim or 384)
    
    if embedding_dim <= 0:
        raise ValueError(f"Invalid embedding dimension: {embedding_dim}")
    
    return embeddings_array, embedding_dim
