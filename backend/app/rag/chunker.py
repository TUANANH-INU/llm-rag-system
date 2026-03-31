"""
Text chunking module
"""
from typing import List, Dict, Any
from pydantic import BaseModel


class Chunk(BaseModel):
    """Text chunk model"""
    content: str
    metadata: Dict[str, Any]


class TextChunker:
    """Split documents into manageable chunks"""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        """
        Initialize chunker
        
        Args:
            chunk_size: Characters per chunk
            overlap: Overlap between chunks for context
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[Chunk]:
        """
        Split text into chunks
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to chunks
        
        Returns:
            List of chunks
        """
        chunks = []
        
        # Split by sentences first for better semantics
        sentences = self._split_sentences(text)
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk.strip():
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_id"] = chunk_index
                    chunks.append(
                        Chunk(
                            content=current_chunk.strip(),
                            metadata=chunk_metadata
                        )
                    )
                    chunk_index += 1
                
                # Start new chunk with overlap
                overlap_sentences = self._get_overlap_sentences(
                    sentences, sentence, chunk_index
                )
                current_chunk = overlap_sentences + " " + sentence
        
        # Add remaining chunk
        if current_chunk.strip():
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = chunk_index
            chunks.append(
                Chunk(
                    content=current_chunk.strip(),
                    metadata=chunk_metadata
                )
            )
        
        return chunks
    
    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        import re
        text = text.replace('\n', ' ')
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def _get_overlap_sentences(sentences: List[str], current: str, chunk_index: int) -> str:
        """Get overlap from previous chunk"""
        overlap_text = ""
        char_count = 0
        
        # Build overlap from 2-3 previous sentences
        for sentence in reversed(sentences):
            if char_count >= 100:  # Minimum overlap
                break
            overlap_text = sentence + " " + overlap_text
            char_count += len(sentence)
        
        return overlap_text.strip()


def create_chunks(documents: List, chunk_size: int = 512, overlap: int = 64) -> List[Chunk]:
    """
    Create chunks from documents
    
    Args:
        documents: List of Document objects
        chunk_size: Characters per chunk
        overlap: Overlap between chunks
    
    Returns:
        List of chunks
    """
    chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
    all_chunks = []
    
    for doc in documents:
        chunks = chunker.chunk(doc.content, doc.metadata)
        all_chunks.extend(chunks)
    
    return all_chunks
