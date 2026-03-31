"""
Vector Store using FAISS
"""
import os
import json
import pickle
from typing import List, Dict, Tuple, Any
import numpy as np
import faiss


class FAISSVectorStore:
    """Vector store using FAISS for similarity search"""
    
    def __init__(self, embedding_dim: int = 384):
        """
        Initialize FAISS vector store
        
        Args:
            embedding_dim: Dimension of embedding vectors
        """
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks_metadata = []
        self.chunk_texts = []
    
    def add_vectors(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]], 
                   texts: List[str]) -> None:
        """
        Add vectors to the store
        
        Args:
            embeddings: Array of embeddings (shape: [n, embedding_dim])
            metadata: List of metadata dicts for each embedding
            texts: List of text chunks
        """
        # Ensure embeddings are float32
        embeddings = embeddings.astype(np.float32)
        
        # Add to index
        self.index.add(embeddings)
        
        # Store metadata and texts
        self.chunks_metadata.extend(metadata)
        self.chunk_texts.extend(texts)
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> Tuple[List[Dict], List[float]]:
        """
        Search for similar vectors
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
        
        Returns:
            Tuple of (results, distances)
        """
        query_embedding = query_embedding.astype(np.float32).reshape(1, -1)
        
        distances, indices = self.index.search(query_embedding, min(k, len(self.chunk_texts)))
        
        results = []
        result_distances = []
        
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks_metadata):
                result = {
                    "text": self.chunk_texts[idx],
                    "metadata": self.chunks_metadata[idx],
                    "score": 1 / (1 + distance)  # Convert distance to similarity score
                }
                results.append(result)
                result_distances.append(float(distance))
        
        return results, result_distances
    
    def save(self, path: str) -> None:
        """Save vector store to disk"""
        os.makedirs(path, exist_ok=True)
        
        # Save index
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))
        
        # Save metadata and texts
        with open(os.path.join(path, "metadata.pkl"), "wb") as f:
            pickle.dump(self.chunks_metadata, f)
        
        with open(os.path.join(path, "texts.pkl"), "wb") as f:
            pickle.dump(self.chunk_texts, f)
        
        # Save config
        config = {
            "embedding_dim": self.embedding_dim,
            "num_vectors": len(self.chunk_texts)
        }
        with open(os.path.join(path, "config.json"), "w") as f:
            json.dump(config, f)
    
    @classmethod
    def load(cls, path: str) -> "FAISSVectorStore":
        """Load vector store from disk"""
        # Load config
        with open(os.path.join(path, "config.json"), "r") as f:
            config = json.load(f)
        
        # Create instance
        store = cls(embedding_dim=config["embedding_dim"])
        
        # Load index
        store.index = faiss.read_index(os.path.join(path, "index.faiss"))
        
        # Load metadata and texts
        with open(os.path.join(path, "metadata.pkl"), "rb") as f:
            store.chunks_metadata = pickle.load(f)
        
        with open(os.path.join(path, "texts.pkl"), "rb") as f:
            store.chunk_texts = pickle.load(f)
        
        return store
