"""
FastAPI API routes for document processing
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
from pydantic import BaseModel
import os
import shutil
from ..rag.loader import DocumentLoader


router = APIRouter(prefix="/api/documents", tags=["documents"])

# Temporary upload directory
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentResponse(BaseModel):
    """Document response model"""
    id: str
    name: str
    type: str
    source: str
    size: int


class URLRequest(BaseModel):
    """URL request model"""
    url: str


@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file
    
    Args:
        file: PDF file
    
    Returns:
        Document information
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Load and verify
        try:
            docs = DocumentLoader.load_pdf(file_path)
            num_pages = len(docs)
        except Exception as e:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
        
        return {
            "id": file.filename,
            "name": file.filename,
            "type": "pdf",
            "source": file_path,
            "size": file_size,
            "pages": num_pages,
            "status": "uploaded"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load-url/")
async def load_url(request: URLRequest):
    """
    Load content from a URL
    
    Args:
        request: URL request
    
    Returns:
        Document information
    """
    try:
        # Validate URL
        if not request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL")
        
        # Load webpage
        try:
            docs = DocumentLoader.load_web(request.url)
            if not docs:
                raise ValueError("Could not extract content from URL")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error loading URL: {str(e)}")
        
        return {
            "id": request.url,
            "name": request.url,
            "type": "web",
            "source": request.url,
            "size": len(docs[0].content) if docs else 0,
            "status": "loaded"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/")
async def list_documents():
    """List uploaded documents"""
    documents = []
    
    if os.path.exists(UPLOAD_DIR):
        for file in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, file)
            if os.path.isfile(file_path):
                documents.append({
                    "name": file,
                    "size": os.path.getsize(file_path),
                    "type": "pdf"
                })
    
    return {"documents": documents}


@router.delete("/delete/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    try:
        file_path = os.path.join(UPLOAD_DIR, document_id)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Document not found")
        
        os.remove(file_path)
        
        return {"status": "deleted", "document_id": document_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
