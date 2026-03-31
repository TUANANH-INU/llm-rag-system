"""
FastAPI API routes for RAG queries
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/rag", tags=["rag"])

# Global RAG system instance (will be initialized in main.py)
rag_system = None

logger = logging.getLogger(__name__)


class QueryRequest(BaseModel):
    """Query request model"""

    question: str
    k: int = 5  # Number of documents to retrieve


class QueryResponse(BaseModel):
    """Query response model"""

    answer: str
    sources: List[str]
    retrieved_docs: int
    confidence: float


class DocumentAddRequest(BaseModel):
    """Request to add documents"""

    pdf_path: Optional[str] = None
    url: Optional[str] = None


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the RAG system

    Args:
        request: Query request

    Returns:
        Answer with sources and citations
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")

        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Query the system
        result = rag_system.query(request.question, k=request.k)

        return QueryResponse(
            answer=result["answer"], sources=result["sources"], retrieved_docs=result["retrieved_docs"], confidence=result["confidence"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-pdf")
async def add_pdf(pdf_path: str):
    """
    Add PDF to RAG system

    Args:
        pdf_path: Path to PDF file

    Returns:
        Status
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")

        rag_system.load_pdf(pdf_path)

        return {"status": "success", "message": "PDF added to RAG system", "path": pdf_path}

    except Exception as e:
        logger.error(f"Error adding PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-url")
async def add_url(url: str):
    """
    Add URL content to RAG system

    Args:
        url: URL

    Returns:
        Status
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")

        rag_system.load_web(url)

        return {"status": "success", "message": "URL content added to RAG system", "url": url}

    except Exception as e:
        logger.error(f"Error adding URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_vector_store(path: str = "data/vector_store"):
    """Save vector store"""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")

        rag_system.save_vector_store(path)

        return {"status": "success", "message": "Vector store saved", "path": path}

    except Exception as e:
        logger.error(f"Error saving vector store: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load")
async def load_vector_store(path: str = "data/vector_store"):
    """Load vector store"""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")

        rag_system.load_vector_store(path)

        return {"status": "success", "message": "Vector store loaded", "path": path}

    except Exception as e:
        logger.error(f"Error loading vector store: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get RAG system status"""
    try:
        if not rag_system:
            return {"status": "not_initialized"}

        return {
            "status": "ready",
            "documents_loaded": len(rag_system.documents),
            "chunks": len(rag_system.chunks),
            "llm_model": rag_system.llm_model,
            "embedding_model": rag_system.embedding_model,
        }

    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def set_rag_system(system):
    """Set the global RAG system instance"""
    global rag_system
    rag_system = system
