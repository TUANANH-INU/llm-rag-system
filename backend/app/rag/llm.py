"""
LLM integration with Ollama
"""
from typing import List, Optional, Dict, Any
import requests
import json


class OllamaLLM:
    """Interface with Ollama LLM"""
    
    def __init__(self, model: str = "llama2", base_url: str = None):
        """
        Initialize Ollama LLM
        
        Args:
            model: Model name (llama2, neural-chat, mistral, etc.)
            base_url: Ollama server base URL
        """
        import os
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    
    def generate(self, prompt: str, temperature: float = 0.7, 
                max_tokens: int = 512, stream: bool = False) -> str:
        """
        Generate text using the LLM
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
        
        Returns:
            Generated text
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "stream": False
                },
                timeout=300
            )
            response.raise_for_status()
            
            # Parse response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    full_response += data.get("response", "")
            
            return full_response.strip()
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")
    
    def generate_with_context(self, query: str, context: List[Dict[str, Any]], 
                            temperature: float = 0.7, 
                            max_tokens: int = 256) -> tuple:
        """
        Generate answer based on query and context
        
        Args:
            query: User query
            context: List of context documents from retriever
            temperature: Sampling temperature
            max_tokens: Maximum tokens
        
        Returns:
            Tuple of (answer, sources)
        """
        # Build context string
        context_str = self._build_context_string(context)
        
        # Build prompt with instructions
        prompt = self._build_rag_prompt(query, context_str)
        
        # Generate answer
        answer = self.generate(prompt, temperature=temperature, max_tokens=max_tokens)
        
        # Extract sources
        sources = [doc["metadata"]["source"] for doc in context]
        
        return answer, sources
    
    @staticmethod
    def _build_context_string(context: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents"""
        context_str = ""
        for i, doc in enumerate(context, 1):
            context_str += f"\n[Document {i}]\n"
            context_str += f"Source: {doc['metadata'].get('source', 'Unknown')}\n"
            context_str += f"Content: {doc['text']}\n"
        return context_str
    
    @staticmethod
    def _build_rag_prompt(query: str, context: str) -> str:
        """Build RAG prompt"""
        prompt = f"""You are a helpful assistant that answers questions based on provided context.

Context:
{context}

Question: {query}

Instructions:
1. Answer the question based ONLY on the provided context
2. If you find the answer in the context, provide it with citations
3. If the answer is not in the context, say "I cannot find this information in the provided sources"
4. Always cite which document/source your answer comes from
5. Be concise and clear

Answer:"""
        return prompt


class RAGPipeline:
    """Complete RAG pipeline"""
    
    def __init__(self, llm_model: str = "llama2", 
                embedding_model: str = "nomic-embed-text"):
        """Initialize RAG pipeline"""
        self.llm = OllamaLLM(model=llm_model)
        self.embedding_model = embedding_model
    
    def answer(self, query: str, retrieved_context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate answer with citations
        
        Args:
            query: User question
            retrieved_context: Context from retriever
        
        Returns:
            Dictionary with answer and citations
        """
        answer, sources = self.llm.generate_with_context(query, retrieved_context)
        
        return {
            "answer": answer,
            "sources": sources,
            "retrieved_docs": len(retrieved_context),
            "confidence": self._calculate_confidence(retrieved_context)
        }
    
    @staticmethod
    def _calculate_confidence(context: List[Dict[str, Any]]) -> float:
        """Calculate confidence score"""
        if not context:
            return 0.0
        
        scores = [doc.get("score", 0) for doc in context]
        return sum(scores) / len(scores) if scores else 0.0
