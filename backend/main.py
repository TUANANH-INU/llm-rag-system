"""
FastAPI main application
"""

import logging
import os

import uvicorn
from app.api import documents, rag
from app.rag.pipeline import RAGSystem
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="RAG Chatbot API", description="Retrieval Augmented Generation Chatbot", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize RAG system
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    try:
        logger.info("Initializing RAG system...")

        llm_model = os.getenv("LLM_MODEL", "llama2")
        embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

        global_rag_system = RAGSystem(llm_model=llm_model, embedding_model=embedding_model, vector_store_path="data/vector_store")

        # Set the RAG system for API routes
        rag.set_rag_system(global_rag_system)

        logger.info(f"RAG system initialized with LLM: {llm_model}, Embedding: {embedding_model}")

        # Try to load existing vector store if available
        if os.path.exists("data/vector_store"):
            try:
                global_rag_system.load_vector_store("data/vector_store")
                logger.info("Loaded existing vector store")
            except Exception as e:
                logger.warning(f"Could not load vector store: {e}")

    except Exception as e:
        logger.error(f"Error initializing RAG system: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down RAG system...")


# Include routers
app.include_router(documents.router)
app.include_router(rag.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "RAG Chatbot API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))

    uvicorn.run("main:app", host=host, port=port, reload=os.getenv("RELOAD", "false").lower() == "true")
